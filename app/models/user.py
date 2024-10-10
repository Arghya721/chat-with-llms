"""User model."""

from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    """Model for user."""

    email: str
    username: str
    profile_picture: str
    google_user_id: str
    created_at: datetime = None
