from app.core.config import get_settings
from app.ai.local import LocalAIEngine
from app.ai.gemini import GeminiEngine

settings = get_settings()


def get_ai_engine():
    """
    Resolve and return the configured AI engine.

    This function is deployment-critical:
    - Enforces explicit provider selection
    - Fails fast on misconfiguration
    - Prevents silent fallbacks in production
    """

    provider = settings.AI_PROVIDER.lower()

    # --------------------------------------------------
    # Gemini (primary, production)
    # --------------------------------------------------
    if provider == "gemini":
        if not settings.GEMINI_API_KEY:
            raise RuntimeError(
                "AI_PROVIDER=gemini but GEMINI_API_KEY is not set"
            )
        return GeminiEngine()

    # --------------------------------------------------
    # Local (development / fallback)
    # --------------------------------------------------
    if provider == "local":
        return LocalAIEngine()

    # --------------------------------------------------
    # Unknown provider (FAIL FAST)
    # --------------------------------------------------
    raise RuntimeError(
        f"Unsupported AI_PROVIDER '{settings.AI_PROVIDER}'. "
        "Valid options: 'gemini', 'local'."
    )
