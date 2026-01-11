from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # --------------------------------------------------
    # Application
    # --------------------------------------------------
    APP_NAME: str = "Goku AI v3 - Auth Service"
    APP_VERSION: str = "1.0.0"
    ENV: str = Field(..., description="Environment name (production, staging, dev)")

    # --------------------------------------------------
    # Security / JWT (REQUIRED)
    # --------------------------------------------------
    JWT_SECRET_KEY: str = Field(..., description="JWT signing secret")
    JWT_ALGORITHM: str = Field(..., description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., description="JWT expiry in minutes")

    # --------------------------------------------------
    # Database (REQUIRED)
    # --------------------------------------------------
    DATABASE_URL: str = Field(..., description="PostgreSQL connection string")

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
