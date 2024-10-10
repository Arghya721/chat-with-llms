import razorpay
from config import settings
import hmac
import hashlib

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


async def create_razorpay_order(amount: int, receipt: str):
    order_data = {
        "amount": amount * 100,  # Amount in paise
        "currency": "INR",
        "receipt": receipt,
    }
    return client.order.create(data=order_data)


async def verify_razorpay_payment(order_id: str, payment_id: str, signature: str):
    generated_signature = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode("utf-8"),
        f"{order_id}|{payment_id}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return generated_signature == signature


async def get_razorpay_order(order_id: str):
    return client.order.fetch(order_id)


async def get_razorpay_payment(payment_id: str):
    return client.payment.fetch(payment_id)
