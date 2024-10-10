"""
Chat controller module for handling chat-related operations.

This module contains functions for processing chat requests, generating responses,
and managing chat-related data.
"""

from fastapi import HTTPException, status, Depends
from models.chat import ChatRequest, ChatEventStreaming, ChatResponse
from services.chat_service import ChatService
from services.database_service import DatabaseService
from controllers.auth_controller import verify_token
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
import json
from fastapi.encoders import jsonable_encoder


class ChatController:
    """Controller for handling chat-related operations."""

    def __init__(self, chat_service: ChatService, database_service: DatabaseService):
        """
        Initialize the ChatController.

        Args:
            chat_service (ChatService): Service for chat-related operations.
            database_service (DatabaseService): Service for database operations.
        """
        self.chat_service = chat_service
        self.database_service = database_service

    async def chat_event_streaming(self, request: ChatRequest, token_info: dict):
        """
        Process a chat request and return a streaming response.

        Args:
            request (ChatRequest): The chat request containing user input and chat history.
            token_info (dict): Information about the authenticated user.

        Returns:
            function: An asynchronous generator for streaming the chat response.

        Raises:
            HTTPException: If there's an error processing the request.
        """
        try:
            chat_model = request.chat_model
            chat = self.chat_service.get_chat_model(chat_model, request.temperature)

            generations_left = await self.database_service.get_generations(
                token_info["sub"]
            )
            if generations_left == 0:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Generations limit exceeded",
                )

            prompt = ChatPromptTemplate(
                messages=[
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessagePromptTemplate.from_template("{user_input}"),
                ]
            )
            memory = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )
            parser = StrOutputParser()

            conversation = prompt | chat | parser

            for chat_history in request.chat_history:
                memory.chat_memory.add_user_message(chat_history.user_message)
                memory.chat_memory.add_ai_message(chat_history.ai_message)

            generated_ai_message = ""
            total_input = prompt.format(
                chat_history=memory.buffer, user_input=request.user_input
            )

            async def event_streaming():
                nonlocal generated_ai_message
                try:
                    for token in conversation.stream(
                        {
                            "chat_history": memory.buffer,
                            "user_input": request.user_input,
                        }
                    ):
                        generated_ai_message += token
                        response = ChatEventStreaming(
                            event="stream", data=token, is_final=False
                        )
                        yield f"data: {json.dumps(jsonable_encoder(response))}\n\n"

                    input_token_length, output_token_length, cost = (
                        self.chat_service.calculate_cost(
                            total_input, generated_ai_message, chat_model
                        )
                    )

                    stats = {
                        "input_token_length": input_token_length,
                        "output_token_length": output_token_length,
                        "cost": cost,
                    }
                    chat_id = await self.database_service.add_message_to_db(
                        request,
                        token_info["sub"],
                        request.user_input,
                        generated_ai_message,
                        stats,
                    )

                    await self.database_service.update_generations_left(
                        token_info["sub"], generations_left
                    )

                    response = ChatEventStreaming(
                        event="stream", data="", is_final=True, chat_id=chat_id
                    )
                    yield f"data: {json.dumps(jsonable_encoder(response))}\n\n"
                except Exception as e:
                    # Log the exception and handle it appropriately
                    print(f"Error in event streaming: {str(e)}")

            return event_streaming()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(e)}"
            )

    async def generate_chat_title(self, request: ChatRequest, token_info: dict):
        """
        Generate a title for a chat conversation.

        Args:
            request (ChatRequest): The chat request containing the conversation history.
            token_info (dict): Information about the authenticated user.

        Returns:
            ChatResponse: The generated chat title.

        Raises:
            HTTPException: If there's an error generating the title.
        """
        try:
            chat = self.chat_service.get_chat_model("gpt-4o-mini", request.temperature)

            generations_left = await self.database_service.get_generations(
                token_info["sub"]
            )
            if generations_left == 0:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Generations limit exceeded",
                )

            prompt = ChatPromptTemplate(
                messages=[
                    MessagesPlaceholder(variable_name="chat_history"),
                    HumanMessagePromptTemplate.from_template("{user_input}"),
                ]
            )
            memory = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )
            conversation = self.chat_service.create_conversation(chat, memory, prompt)

            for chat_history in request.chat_history:
                memory.chat_memory.add_user_message(chat_history.user_message)
                memory.chat_memory.add_ai_message(chat_history.ai_message)

            response = conversation.invoke(
                input="Generate a concise and relevant 5-word title for the above chat based on the main topic discussed. Do not include any creative or ambiguous terms."
            )

            response["text"] = response["text"].replace('"', "").replace("/", "")

            await self.database_service.update_chat_title(
                request.chat_id, response["text"]
            )

            return ChatResponse(response=response["text"])
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(e)}"
            )
