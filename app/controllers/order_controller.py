"""This module contains the controller functions for the order endpoints."""

from fastapi import HTTPException, status, Depends
from models.order import PaymentRequest
from services.payment_service import create_razorpay_order, verify_razorpay_payment
from services.database import (
    add_order_to_db,
    add_payment_to_db,
    get_generations,
    update_user_generations,
)
from controllers.auth_controller import verify_token
from config import settings


async def create_order(plan_id: str, token_info: dict = Depends(verify_token)):
    """Create an order for the given plan."""
    try:
        if not settings.ENABLE_PAYMENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Payment is disabled",
            )

        amount = 0
        if plan_id == "plan_50":
            amount = 399
        elif plan_id == "plan_150":
            amount = 899
        elif plan_id == "plan_300":
            amount = 1799
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid plan id",
            )

        order = await create_razorpay_order(amount, plan_id)
        await add_order_to_db(order["id"], plan_id, token_info["sub"])

        return {
            "order_id": order["id"],
            "amount": amount,
            "currency": "INR",
            "receipt": plan_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


async def verify_payment(
    request: PaymentRequest, token_info: dict = Depends(verify_token)
):
    """Verify the payment and update user generations."""
    try:
        if not settings.ENABLE_PAYMENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Payment is disabled",
            )

        payment_exists = await check_payment_exists(request.razorpay_payment_id)
        if payment_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already exists",
            )

        is_valid = await verify_razorpay_payment(
            request.razorpay_order_id,
            request.razorpay_payment_id,
            request.razorpay_signature,
        )
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature",
            )

        order_data = await get_razorpay_order(request.razorpay_order_id)
        if order_data["status"] == "paid":
            await add_payment_to_db(
                request.razorpay_order_id,
                request.razorpay_payment_id,
                token_info["sub"],
            )

            generations_left = await get_generations(token_info["sub"])
            additional_generations = 0
            if order_data["receipt"] == "plan_50":
                additional_generations = 50
            elif order_data["receipt"] == "plan_250":
                additional_generations = 250
            elif order_data["receipt"] == "plan_500":
                additional_generations = 500

            await update_user_generations(
                token_info["sub"], generations_left + additional_generations
            )

            return {"status": "success"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment failed",
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
