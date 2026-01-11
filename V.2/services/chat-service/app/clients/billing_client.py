import requests
from app.core.config import get_settings


class BillingLimitExceeded(Exception):
    """Raised when user exceeds billing limits."""


class BillingServiceClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.BILLING_SERVICE_URL.rstrip("/")

    def record_usage(self, user_id: str, endpoint: str, tokens: int = 1) -> None:
        response = requests.post(
            f"{self.base_url}/usage/record",
            json={
                "user_id": user_id,
                "endpoint": endpoint,
                "tokens": tokens,
            },
            timeout=5,
        )

        # HARD BLOCK
        if response.status_code == 429:
            raise BillingLimitExceeded("Usage limit exceeded")

        if response.status_code != 200:
            raise RuntimeError(
                f"Billing service error: {response.status_code} {response.text}"
            )
