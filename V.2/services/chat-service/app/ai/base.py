from abc import ABC, abstractmethod
from typing import Dict


class AIEngine(ABC):
    """
    Abstract base class for AI engines.
    """

    @abstractmethod
    def generate_reply(
        self,
        message: str,
        persona: str,
        user_context: Dict,
    ) -> str:
        """
        Generate a reply from the AI model.
        """
        raise NotImplementedError
