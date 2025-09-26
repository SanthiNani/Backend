# backend/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


# Load .env file
load_dotenv()

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-strong-jwt-secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRY_MINUTES: int = int(os.getenv("JWT_EXPIRY_MINUTES", 1440))

    # Hugging Face
    HUGGINGFACE_API_KEY: str = os.getenv("HF_API_KEY", "")
    HUGGINGFACE_MODEL_NAME: str = os.getenv("HF_MODEL", "distilbert-base-uncased")
    print("Hugging Face API Key:", HUGGINGFACE_API_KEY)


    # Redis (ensure REDIS_PASSWORD defaults to empty string if None)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD") or ""

    # Project
    APP_NAME: str = "HealthAI Backend"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ["true", "1", "yes"]

# Create singleton settings object
settings = Settings()
