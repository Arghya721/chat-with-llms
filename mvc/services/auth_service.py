from fastapi import HTTPException, status, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
from jose import jwt
from google.cloud import firestore as google_firestore
import firebase_admin
from firebase_admin import firestore
from .utils import get_environment_variable

# Firebase initialization is assumed to be done in main application
# Create Firestore client
if firebase_admin._apps:
    db = firestore.client()
else:
    cred = firebase_admin.credentials.Certificate("serviceAccount.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

SECRET_KEY = get_environment_variable("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

auth_scheme = HTTPBearer()

async def add_user_to_db(user_ref, user_data):
    """Add or update the user in Firestore."""
    user = user_ref.get()
    if user.exists:
        return
    user_data['created_at'] = google_firestore.SERVER_TIMESTAMP
    user_ref.set(user_data)

async def verify_google_token(background_tasks: BackgroundTasks, credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """Verify the Google ID token and return the user info."""
    if credentials:
        token = credentials.credentials
        try:
            request = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            request.raise_for_status()
            credentials_info = request.json()
            user_ref = db.collection('users').document(credentials_info['sub'])
            user_data = {
                'email': credentials_info['email'],
                'username': credentials_info['name'],
                'profile_picture': credentials_info['picture'],
                'google_user_id': credentials_info['sub'],
            }
            background_tasks.add_task(add_user_to_db, user_ref, user_data)
            return credentials_info
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired Google ID token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Verify the JWT token and return the user info."""
    if credentials:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            ) from exc
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
