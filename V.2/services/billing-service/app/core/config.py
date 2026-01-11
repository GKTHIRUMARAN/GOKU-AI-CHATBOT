from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --------------------------------------------------
    # Application
    # --------------------------------------------------
    APP_NAME: str = "Goku AI v3 - Billing Service"
    APP_VERSION: str = "1.0.0"
    ENV: str = Field(..., description="Environment name")

    # --------------------------------------------------
    # Database
    # --------------------------------------------------
    DATABASE_URL: str = Field(
        ...,
        description="PostgreSQL connection URL",
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
