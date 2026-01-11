from functools import lru_cache
from typing import Literal, Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -------------------------------------------------
    # App
    # -------------------------------------------------
    APP_NAME: str = "Goku AI v3 - Chat Service"
    APP_VERSION: str = "1.0.0"
    ENV: Literal["development", "staging", "production"] = "development"

    # -------------------------------------------------
    # Auth / Security
    # -------------------------------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    # -------------------------------------------------
    # AI Provider Selection
    # -------------------------------------------------
    AI_PROVIDER: Literal["local", "gemini", "openai"] = "gemini"

    # -------------------------------------------------
    # Gemini (Google)
    # -------------------------------------------------
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "models/gemini-2.5-flash"

    # -------------------------------------------------
    # OpenAI (optional fallback)
    # -------------------------------------------------
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # -------------------------------------------------
    # Internal Services
    # -------------------------------------------------
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    MEMORY_SERVICE_URL: str = "http://memory-service:8003"
    BILLING_SERVICE_URL: str = "http://billing-service:8004"

    # -------------------------------------------------
    # Chat / Memory limits
    # -------------------------------------------------
    MAX_CONTEXT_MESSAGES: int = 10
    MAX_LONG_TERM_ENTRIES: int = 5

    # -------------------------------------------------
    # 🔐 HARD VALIDATION (FAIL FAST)
    # -------------------------------------------------
    @model_validator(mode="after")
    def validate_provider_config(self) -> "Settings":
        if self.AI_PROVIDER == "gemini":
            if not self.GEMINI_API_KEY:
                raise ValueError(
                    "AI_PROVIDER=gemini requires GEMINI_API_KEY to be set"
                )

        if self.AI_PROVIDER == "openai":
            if not self.OPENAI_API_KEY:
                raise ValueError(
                    "AI_PROVIDER=openai requires OPENAI_API_KEY to be set"
                )

        return self

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    App will FAIL ON STARTUP if config is invalid.
    """
    return Settings()
