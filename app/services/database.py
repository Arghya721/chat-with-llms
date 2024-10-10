from google.cloud import firestore
from models.user import User
from models.chat import ChatRequest, ChatUserHistory, ChatByIdHistory
from config import settings
import firebase_admin
from firebase_admin import credentials, firestore
import uuid

if settings.ENVIRONMENT == "dev":
    cred = credentials.Certificate("serviceAccount.json")
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()

db = firestore.client()


async def add_user_to_db(user: User):
    user_ref = db.collection("users").document(user.google_user_id)
    user_data = user.dict()
    if not user_ref.get().exists:
        user_data["created_at"] = firestore.SERVER_TIMESTAMP
        user_ref.set(user_data)


async def add_message_to_db(
    request: ChatRequest,
    google_user_id: str,
    user_message: str,
    ai_message: str,
    stats: dict,
):
    chat_id = request.chat_id or str(uuid.uuid4())
    chat_ref = db.collection("chats").document(chat_id)

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

    db.collection("chat_history").add(
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


async def get_generations(google_user_id: str):
    user_generations_ref = db.collection("user_generations").document(google_user_id)
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


async def update_generations_left(google_user_id: str, generations_left: int):
    user_generations_ref = db.collection("user_generations").document(google_user_id)
    user_generations_ref.update(
        {
            "remaining_generations": generations_left - 1,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
    )


async def update_chat_title(chat_id: str, new_chat_title: str):
    chat_doc_ref = db.collection("chats").document(chat_id)
    chat_doc_ref.update(
        {
            "chat_title": new_chat_title,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
    )


async def get_user_chat_history(google_user_id: str, page: int, limit: int):
    start_index = (page - 1) * limit
    chat_ref = (
        db.collection("chats")
        .where("google_user_id", "==", google_user_id)
        .order_by("updated_at", direction=firestore.Query.DESCENDING)
        .offset(start_index)
        .limit(limit)
        .stream()
    )
    return [ChatUserHistory(**chat.to_dict()) for chat in chat_ref]


async def get_chat_by_id(chat_id: str, google_user_id: str):
    chat_ref = db.collection("chats").document(chat_id).get()
    if not chat_ref.exists or chat_ref.to_dict()["google_user_id"] != google_user_id:
        raise ValueError("Chat not found or access denied")

    chat_history_ref = (
        db.collection("chat_history").where("chat_id", "==", chat_id).stream()
    )
    return [ChatByIdHistory(**chat.to_dict()) for chat in chat_history_ref]


async def add_order_to_db(order_id: str, plan_id: str, google_user_id: str):
    db.collection("orders").add(
        {
            "order_id": order_id,
            "plan_id": plan_id,
            "customer_id": google_user_id,
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
    )


async def add_payment_to_db(order_id: str, payment_id: str, google_user_id: str):
    db.collection("payments").add(
        {
            "order_id": order_id,
            "payment_id": payment_id,
            "customer_id": google_user_id,
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
    )


async def update_user_generations(google_user_id: str, new_generations: int):
    user_generations_ref = db.collection("user_generations").document(google_user_id)
    user_generations_ref.update(
        {
            "remaining_generations": new_generations,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
    )


async def fetch_user_payments(google_user_id: str):
    payments_ref = (
        db.collection("payments")
        .where("customer_id", "==", google_user_id)
        .order_by("updated_at", direction=firestore.Query.DESCENDING)
        .stream()
    )
    return [payment.to_dict() for payment in payments_ref]


async def fetch_payment_details(payment_id: str, google_user_id: str):
    payment_ref = (
        db.collection("payments")
        .where("payment_id", "==", payment_id)
        .where("customer_id", "==", google_user_id)
        .limit(1)
        .get()
    )
    if not payment_ref:
        raise ValueError("Payment not found")
    return payment_ref[0].to_dict()
