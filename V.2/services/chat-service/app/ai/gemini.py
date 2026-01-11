from typing import List, Dict

from google import genai
from google.genai.errors import ServerError, ClientError

from app.ai.retry import retry_with_backoff
from app.core.config import get_settings

settings = get_settings()


class GeminiEngine:
    """
    Gemini AI engine with:
    - Persona grounding
    - Memory grounding
    - Retry + graceful degradation
    - Deployment-safe error handling
    """

    def __init__(self) -> None:
        # Fail-fast already enforced by Settings validator
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL

    def generate_reply(
        self,
        persona_prompt: str,
        long_term_memory: List[str],
        conversation_messages: List[Dict[str, str]],
        user_message: str,
    ) -> str:
        """
        Generate a response using Gemini with grounded context.
        """

        prompt_parts: List[str] = []

        # --------------------------------------------------
        # 1️⃣ Persona grounding (MANDATORY)
        # --------------------------------------------------
        prompt_parts.append(persona_prompt.strip())

        # --------------------------------------------------
        # 2️⃣ Long-term memory grounding (OPTIONAL)
        # --------------------------------------------------
        if long_term_memory:
            memory_block = "\n".join(f"- {m}" for m in long_term_memory)
            prompt_parts.append(
                "Known facts about the user:\n" + memory_block
            )

        # --------------------------------------------------
        # 3️⃣ Conversation history (short-term memory)
        # --------------------------------------------------
        for msg in conversation_messages:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            prompt_parts.append(f"{role}: {content}")

        # --------------------------------------------------
        # 4️⃣ Current user message
        # --------------------------------------------------
        prompt_parts.append(f"User: {user_message}")

        final_prompt = "\n\n".join(prompt_parts)

        # --------------------------------------------------
        # 5️⃣ Gemini call (wrapped for retry)
        # --------------------------------------------------
        def _call_gemini() -> str:
            response = self.client.models.generate_content(
                model=self.model,
                contents=final_prompt,
            )

            # Defensive: response.text is not guaranteed
            if not response or not getattr(response, "text", None):
                raise RuntimeError("Empty response from Gemini")

            return response.text.strip()

        try:
            return retry_with_backoff(_call_gemini)

        # --------------------------------------------------
        # 6️⃣ Graceful degradation (NO crashes)
        # --------------------------------------------------
        except ServerError:
            return (
                "I'm experiencing heavy load right now. "
                "Please try again in a moment."
            )

        except ClientError:
            return (
                "I encountered a configuration issue while responding. "
                "Please contact support."
            )

        except Exception:
            # Absolute last-resort safety net
            return (
                "Something went wrong while generating a response. "
                "Please try again shortly."
            )
