from abc import ABC, abstractmethod
from typing import Dict, List


class Persona(ABC):
    """
    Base persona contract.
    All personas must implement this interface.
    """

    # -------------------------------
    # Identity
    # -------------------------------

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Unique persona identifier (used by API).
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def display_name(self) -> str:
        """
        Human-readable persona name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Short description of the persona.
        """
        raise NotImplementedError

    # -------------------------------
    # Behavior
    # -------------------------------

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """
        System prompt injected into the AI engine.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def response_rules(self) -> List[str]:
        """
        List of rules guiding response style.
        """
        raise NotImplementedError

    # -------------------------------
    # Capabilities (future-proof)
    # -------------------------------

    @property
    def capabilities(self) -> Dict[str, bool]:
        """
        Feature flags for the persona.
        Defaults are conservative.
        """
        return {
            "use_memory": True,      # enabled by default for chat
            "use_tools": False,
            "generate_code": False,
        }
