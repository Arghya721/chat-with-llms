"""
Database service module for handling database operations.

This module provides an interface for interacting with the database,
abstracting away the specifics of the database implementation.
"""

from google.cloud import firestore
from models.user import User
from models.chat import ChatRequest, ChatUserHistory, ChatByIdHistory
from config import settings
import firebase_admin
from firebase_admin import credentials, firestore
import uuid


class DatabaseService:
    """Service for database-related operations."""

    def __init__(self):
        """Initialize the DatabaseService and set up the database connection."""
        if settings.ENVIRONMENT == "dev":
            cred = credentials.Certificate("serviceAccount.json")
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()

        self.db = firestore.client()

    async def add_user_to_db(self, user: User):
        """
        Add a new user to the database or update an existing user.

        Args:
            user (User): The user object to be added or updated.
        """
        user_ref = self.db.collection("users").document(user.google_user_id)
        user_data = user.dict()
        if not user_ref.get().exists:
            user_data["created_at"] = firestore.SERVER_TIMESTAMP
            user_ref.set(user_data)

    async def add_message_to_db(
        self,
        request: ChatRequest,
        google_user_id: str,
        user_message: str,
        ai_message: str,
        stats: dict,
    ):
        """
        Add a new chat message to the database.

        Args:
            request (ChatRequest): The chat request object.
            google_user_id (str): The Google user ID of the user.
            user_message (str): The message from the user.
            ai_message (str): The response from the AI.
            stats (dict): Statistics about the chat interaction.

        Returns:
            str: The chat ID of the added message.

        Raises:
            ValueError: If access to the chat is forbidden.
        """
        chat_id = request.chat_id or str(uuid.uuid4())
        chat_ref = self.db.collection("chats").document(chat_id)

        if chat_ref.get().exists:
            if chat_ref.get().to_dict()["google_user_id"] != google_user_id:
                raise ValueError("Forbidden")
            chat_ref.update(
                {"updated_at": firestore.SERVER_TIMESTAMP, "model": request.chat_model}
            )
        else:
            chat_ref.set(
                {
                    "chat_id": chat_id,
                    "google_user_id": google_user_id,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "updated_at": firestore.SERVER_TIMESTAMP,
                    "model": request.chat_model,
                }
            )

        self.db.collection("chat_history").add(
            {
                "ai_message": ai_message,
                "user_message": user_message,
                "chat_id": chat_id,
                "created_at": firestore.SERVER_TIMESTAMP,
                "updated_at": firestore.SERVER_TIMESTAMP,
                "regenerate_message": request.regenerate_message,
                "model": request.chat_model,
                "stats": stats,
            }
        )

        return chat_id

    async def get_generations(self, google_user_id: str):
        """
        Get the number of remaining generations for a user.

        Args:
            google_user_id (str): The Google user ID of the user.

        Returns:
            int: The number of remaining generations.
        """
        user_generations_ref = self.db.collection("user_generations").document(
            google_user_id
        )
        user_generations_data = user_generations_ref.get()
        if user_generations_data.exists:
            return user_generations_data.to_dict()["remaining_generations"]
        else:
            user_generations_ref.set(
                {
                    "google_user_id": google_user_id,
                    "remaining_generations": 20,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "updated_at": firestore.SERVER_TIMESTAMP,
                }
            )
            return 20

    async def update_generations_left(self, google_user_id: str, generations_left: int):
        """
        Update the number of remaining generations for a user.

        Args:
            google_user_id (str): The Google user ID of the user.
            generations_left (int): The current number of generations left.
        """
        user_generations_ref = self.db.collection("user_generations").document(
            google_user_id
        )
        user_generations_ref.update(
            {
                "remaining_generations": generations_left - 1,
                "updated_at": firestore.SERVER_TIMESTAMP,
            }
        )

    # ... (implement other methods with similar docstrings and comments)
