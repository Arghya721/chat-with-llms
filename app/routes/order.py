"""This module contains the routes for the order endpoints."""

from fastapi import APIRouter, Depends
from controllers.order_controller import create_order, verify_payment
from controllers.auth_controller import verify_token
from models.order import PaymentRequest
from services.database import fetch_user_payments, fetch_payment_details

router = APIRouter()


@router.post("/create_order")
async def create_order_route(plan_id: str, token_info: dict = Depends(verify_token)):
    """Route for creating an order."""
    return await create_order(plan_id, token_info)


@router.post("/verify_payment")
async def verify_payment_route(
    request: PaymentRequest, token_info: dict = Depends(verify_token)
):
    """Route for verifying payment."""
    return await verify_payment(request, token_info)


@router.get("/fetch_payments")
async def fetch_payments_route(token_info: dict = Depends(verify_token)):
    """Route for fetching user payments."""
    return await fetch_user_payments(token_info["sub"])


@router.get("/fetch_payment/{payment_id}")
async def fetch_payment_route(
    payment_id: str, token_info: dict = Depends(verify_token)
):
    """Route for fetching payment details."""
    return await fetch_payment_details(payment_id, token_info["sub"])
