"""This module contains the routes for the authentication endpoints."""

from fastapi import APIRouter, Depends
from controllers.auth_controller import (
    verify_google_token,
    create_access_token,
    verify_token,
)

router = APIRouter()


@router.get("/google")
async def google_auth(user_info: dict = Depends(verify_google_token)):
    """Authenticate user with Google OAuth2 token."""
    access_token = await create_access_token({"sub": user_info["sub"]})
    return {"accessToken": access_token, "user": user_info, "token_type": "Bearer"}


@router.get("/verify")
async def verify_token_info(token_info: dict = Depends(verify_token)):
    """Verify token information."""
    return {"token_info": token_info}
