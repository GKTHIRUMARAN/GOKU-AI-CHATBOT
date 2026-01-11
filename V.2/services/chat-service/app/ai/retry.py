import time
import random
from typing import Callable

from google.genai.errors import ServerError, ClientError


def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.8,
    max_delay: float = 5.0,
):
    """
    Retry Gemini calls with exponential backoff.
    Retries ONLY on transient server errors.
    """

    attempt = 0

    while True:
        try:
            return fn()

        except ServerError as e:
            # Retryable (503, overload, internal)
            attempt += 1
            if attempt > max_retries:
                raise

            delay = min(
                max_delay,
                base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.3),
            )
            time.sleep(delay)

        except ClientError:
            # NOT retryable (bad request, auth, quota exceeded)
            raise
