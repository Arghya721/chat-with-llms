"""This module contains the routes for chat related operations"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from controllers.chat_controller import ChatController
from controllers.auth_controller import verify_token
from models.chat import ChatRequest, ChatUserHistory, ChatByIdHistory
from services.database import get_user_chat_history, get_chat_by_id, get_generations
from services.chat_service import ChatService
from services.database_service import DatabaseService
from pydantic import ValidationError

router = APIRouter()

@router.post("/chat_event_streaming")
async def chat_event_streaming_route(
    request: ChatRequest, token_info: dict = Depends(verify_token)
):
    """Route for chat event streaming."""
    try:
        chat_controller = ChatController(ChatService, DatabaseService)

        return await chat_controller.chat_event_streaming(request, token_info)
    except ValidationError as ve:
        # Handle validation errors specifically for better user feedback
        logging.error("Validation error: %s", ve)
        raise HTTPException(status_code=400, detail="Invalid request data") from ve
    except HTTPException as he:
        
        logging.error("Error processing chat request: %s", he)
        raise HTTPException(status_code=he.status_code, detail=he.detail) from he
    except Exception as e:
        # Log and handle generic exceptions gracefully
        logging.error("Error processing chat request: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.post("/chat_title")
async def chat_title_route(
    request: ChatRequest, token_info: dict = Depends(verify_token)
):
    """Route for generating chat title."""
    return await ChatController.generate_chat_title(request, token_info)


@router.get("/chat_history", response_model=list[ChatUserHistory])
async def user_chat_history(
    page: int = 1, limit: int = 10, token_info: dict = Depends(verify_token)
):
    """Route for getting user chat history."""
    return await get_user_chat_history(token_info["sub"], page, limit)


@router.get("/chat_by_id", response_model=list[ChatByIdHistory])
async def chat_by_id(chat_id: str, token_info: dict = Depends(verify_token)):
    """Route for getting chat by ID."""
    return await get_chat_by_id(chat_id, token_info["sub"])


@router.get("/generations")
async def get_generations_left(token_info: dict = Depends(verify_token)):
    """Route for getting generations left."""
    generations_left = await get_generations(token_info["sub"])
    return {"generations_left": generations_left}
