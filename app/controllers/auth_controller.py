"""This module contains the functions for authenticating users using Google OAuth2.0 and JWT tokens."""

from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
import requests
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import settings
from models.user import User
from services.database import add_user_to_db

auth_scheme = HTTPBearer()


async def verify_google_token(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """Verify Google OAuth2 token and return user information."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        response.raise_for_status()
        user_info = response.json()

        user = User(
            email=user_info["email"],
            username=user_info["name"],
            profile_picture=user_info["picture"],
            google_user_id=user_info["sub"],
        )

        await add_user_to_db(user)
        return user_info
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Google ID token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


async def create_access_token(data: dict):
    """Create a new JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    """Verify JWT token and return payload."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc
