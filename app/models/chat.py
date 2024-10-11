"""This module contains the pydantic models for the chat API. """

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ChatHistory(BaseModel):
    """Model for chat history."""

    ai_message: str
    user_message: str


class ChatRequest(BaseModel):
    """Model for chat request."""

    user_input: str
    chat_history: list[ChatHistory]
    chat_model: str = "gpt-3.5-turbo"
    temperature: float = 0.8
    chat_id: Optional[str] = None
    regenerate_message: Optional[bool] = False


class ChatResponse(BaseModel):
    """Model for chat response."""

    response: str


class ChatEventStreaming(BaseModel):
    """Model for chat event streaming."""

    event: str
    data: str
    is_final: bool
    chat_id: Optional[str] = None


class ChatUserHistory(BaseModel):
    """Chat user history model for the chat history endpoint."""

    chat_id: str
    chat_title: Optional[str] = None
    chat_model: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ChatByIdHistory(BaseModel):
    """Model for chat by ID history."""

    ai_message: str
    user_message: str
    created_at: datetime
    updated_at: datetime
    regenerate_message: bool
    model: str
