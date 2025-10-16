# backend/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str = Field(..., env="SUPABASE_URL")
    SUPABASE_KEY: str = Field(..., env="SUPABASE_KEY")

    # JWT
    JWT_SECRET: str = Field("your-strong-jwt-secret", env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    JWT_EXPIRY_MINUTES: int = Field(1440, env="JWT_EXPIRY_MINUTES")

    # Hugging Face
    HUGGINGFACE_API_KEY: str = Field(..., env="HUGGINGFACE_API_KEY")
    HUGGINGFACE_MODEL_NAME: str = Field("distilbert-base-uncased", env="HF_MODEL")

    # Redis
    REDIS_HOST: str = Field("localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    REDIS_DB: int = Field(0, env="REDIS_DB")
    REDIS_PASSWORD: str = Field("", env="REDIS_PASSWORD")

    # Project
    APP_NAME: str = "HealthAI Backend"
    DEBUG: bool = Field(True, env="DEBUG")

    # Pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

# Create singleton settings object
settings = Settings()

# Log important info (optional)
logging.info(f"App: {settings.APP_NAME}, Debug: {settings.DEBUG}")
logging.info(f"Hugging Face Model: {settings.HUGGINGFACE_MODEL_NAME}")
