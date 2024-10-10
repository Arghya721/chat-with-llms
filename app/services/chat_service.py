"""
Chat service module for handling chat model operations.

This module provides services for interacting with various chat models
and performing cost calculations.
"""

from config import settings
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatPerplexity
from langchain_together import ChatTogether
from langchain.chains import LLMChain
import tiktoken
from anthropic import Anthropic
from vertexai.preview import tokenization


class ChatService:
    """Service for chat-related operations."""

    def __init__(self):
        """Initialize the ChatService with model configurations."""
        self.model_company_mapping = {
            # ... (keep the existing model_company_mapping dictionary)
        }

    def get_chat_model(self, model_name: str, temperature: float):
        """
        Get the appropriate chat model based on the model name.

        Args:
            model_name (str): The name of the chat model.
            temperature (float): The temperature setting for the model.

        Returns:
            object: An instance of the chat model.

        Raises:
            ValueError: If an invalid chat model is specified.
        """
        chat_config = self.model_company_mapping.get(model_name)
        if not chat_config:
            raise ValueError(f"Invalid chat model: {model_name}")

        return chat_config["model"](
            model_name=model_name,
            model=model_name,
            temperature=temperature,
        )

    def calculate_cost(self, input_string: str, output_string: str, model_name: str):
        """
        Calculate the cost of a chat interaction based on input and output tokens.

        Args:
            input_string (str): The input text.
            output_string (str): The output text.
            model_name (str): The name of the chat model used.

        Returns:
            tuple: A tuple containing (input_token_length, output_token_length, total_cost).
        """
        chat_config = self.model_company_mapping.get(model_name)
        input_token_length = 0
        output_token_length = 0

        if chat_config["company"] == "OpenAI":
            encoding = tiktoken.encoding_for_model(model_name)
            input_token_length = len(encoding.encode(input_string))
            output_token_length = len(encoding.encode(output_string))
        elif chat_config["company"] == "Anthropic":
            anthropic = Anthropic()
            input_token_length = anthropic.count_tokens(input_string)
            output_token_length = anthropic.count_tokens(output_string)
        elif chat_config["company"] in ["Mistral", "Perplexity", "Meta"]:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            input_token_length = len(encoding.encode(input_string))
            output_token_length = len(encoding.encode(output_string))
        elif chat_config["company"] == "Google":
            tokenizer = tokenization.get_tokenizer_for_model("gemini-1.5-flash-001")
            input_token_length = tokenizer.count_tokens(input_string).total_tokens
            output_token_length = tokenizer.count_tokens(output_string).total_tokens

        input_cost = (
            input_token_length * chat_config["input_token_cost_per_million"] / 1000000
        )
        output_cost = (
            output_token_length * chat_config["output_token_cost_per_million"] / 1000000
        )
        return input_token_length, output_token_length, input_cost + output_cost

    def create_conversation(self, chat, memory, prompt):
        """
        Create a conversation chain using the provided chat model, memory, and prompt.

        Args:
            chat: The chat model instance.
            memory: The conversation memory.
            prompt: The chat prompt template.

        Returns:
            LLMChain: A conversation chain for generating responses.
        """
        return LLMChain(llm=chat, memory=memory, prompt=prompt, verbose=False)
