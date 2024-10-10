"""This module contains the routes for chat related operations"""

from fastapi import APIRouter, Depends
from controllers.chat_controller import chat_event_streaming, generate_chat_title
from controllers.auth_controller import verify_token
from models.chat import ChatRequest, ChatUserHistory, ChatByIdHistory
from services.database import get_user_chat_history, get_chat_by_id, get_generations

router = APIRouter()


@router.post("/chat_event_streaming")
async def chat_event_streaming_route(
    request: ChatRequest, token_info: dict = Depends(verify_token)
):
    """Route for chat event streaming."""
    return await chat_event_streaming(request, token_info)


@router.post("/chat_title")
async def chat_title_route(
    request: ChatRequest, token_info: dict = Depends(verify_token)
):
    """Route for generating chat title."""
    return await generate_chat_title(request, token_info)


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
