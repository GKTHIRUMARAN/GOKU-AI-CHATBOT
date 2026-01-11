from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # --------------------------------------------------
    # Application
    # --------------------------------------------------
    APP_NAME: str = "Goku AI v3 - Memory Service"
    APP_VERSION: str = "1.0.0"
    ENV: str = Field(..., description="Environment name")

    # --------------------------------------------------
    # Database
    # --------------------------------------------------
    DATABASE_URL: str = Field(..., description="PostgreSQL connection URL")

    # --------------------------------------------------
    # Memory Limits (safe defaults)
    # --------------------------------------------------
    MAX_CONTEXT_MESSAGES: int = Field(
        default=10,
        description="Number of recent messages returned as short-term memory",
    )

    MAX_LONG_TERM_ENTRIES: int = Field(
        default=5,
        description="Number of long-term memory entries returned",
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings loader.
    Fails fast if required env vars are missing.
    """
    return Settings()
