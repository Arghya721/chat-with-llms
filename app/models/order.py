"""Model for order."""

from pydantic import BaseModel


class PaymentRequest(BaseModel):
    """Model for payment request."""

    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
