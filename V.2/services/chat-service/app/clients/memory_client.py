import httpx
from typing import Dict
from app.core.config import get_settings

settings = get_settings()


class MemoryServiceClient:
    def __init__(self) -> None:
        self.base_url = settings.MEMORY_SERVICE_URL
        self.timeout = 5.0

    def get_context(self, user_id: str, persona_id: str) -> Dict:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.get(
                    f"{self.base_url}/api/v1/memory/context",
                    params={
                        "user_id": user_id,
                        "persona_id": persona_id,
                    },
                )
                resp.raise_for_status()
                return resp.json()
        except Exception:
            # ✅ Never crash chat if memory is unavailable
            return {
                "messages": [],
                "long_term": [],
            }

    def store_message(
        self,
        user_id: str,
        persona_id: str,
        role: str,
        content: str,
    ) -> None:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                client.post(
                    f"{self.base_url}/api/v1/memory/message",
                    json={
                        "user_id": user_id,
                        "persona_id": persona_id,
                        "role": role,
                        "content": content,
                    },
                )
        except Exception:
            pass  # Memory must never crash chat

    def store_long_term_memory(
        self,
        user_id: str,
        persona_id: str,
        content: str,
    ) -> None:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                client.post(
                    f"{self.base_url}/api/v1/memory/long-term",
                    json={
                        "user_id": user_id,
                        "persona_id": persona_id,
                        "content": content,
                    },
                )
        except Exception:
            pass