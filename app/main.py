"""
Main application module for the AI Chat API.

This module initializes the FastAPI application, sets up CORS middleware,
and includes the necessary routers for authentication, chat, and order functionality.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, chat, order
from config import settings


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(chat.router, prefix="/v1", tags=["AI"])
    app.include_router(order.router, prefix="/v1", tags=["Order"])

    return app


app = create_app()

if __name__ == "__main__":
    app = create_app()  # Create the app here again for direct reference

    uvicorn.run(app, host="0.0.0.0", port=settings.PORT, log_level="info")
