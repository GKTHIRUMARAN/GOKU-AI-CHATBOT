from core.config import get_settings
from ai.local import LocalAIEngine
from ai.openai import OpenAIEngine
from ai.base import AIEngine

settings = get_settings()


def get_ai_engine() -> AIEngine:
    """
    Factory for selecting AI backend.
    """
    provider = settings.AI_PROVIDER.lower()

    if provider == "local":
        return LocalAIEngine()

    if provider == "openai":
        return OpenAIEngine()

    raise ValueError(f"Unsupported AI_PROVIDER: {provider}")
