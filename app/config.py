"""Configuration module."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class."""

    SECRET_KEY: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str
    ENABLE_PAYMENT: bool = False
    PORT: int = 5000
    LOG_LEVEL: str = "ERROR"
    ENVIRONMENT: str = "dev"

    class Config:
        """Config class."""
        env_file = ".env"
        extra = "ignore"


settings = Settings()
