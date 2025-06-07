from fastapi import APIRouter, Depends, BackgroundTasks
from jose import jwt
from ..services.auth_service import verify_google_token, verify_token, SECRET_KEY

router = APIRouter(prefix="", tags=["Authentication Endpoints"])

@router.get("/auth/google")
async def google_auth(background_tasks: BackgroundTasks, idinfo: dict = Depends(verify_google_token)):
    """Google authentication endpoint to verify the Google ID token."""
    token = jwt.encode({"sub": idinfo["sub"], "exp": jwt.datetime.datetime.utcnow() + jwt.datetime.timedelta(days=30)}, SECRET_KEY, algorithm="HS256")
    return {"accessToken": token, "user": idinfo, "token_type": "Bearer"}

@router.get("/verify")
async def verify_token_info(token_info: dict = Depends(verify_token)):
    """Verify the JWT token and return the user info."""
    return {"token_info": token_info}
