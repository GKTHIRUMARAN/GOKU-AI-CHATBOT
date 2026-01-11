from app.personas.base import Persona
from app.personas.goku import GokuPersona


# -------------------------------
# Persona Registry
# -------------------------------

_PERSONAS: dict[str, Persona] = {
    "goku": GokuPersona(),
}


def get_persona(persona_id: str) -> Persona:
    """
    Resolve persona by ID.
    Falls back to Goku if invalid or missing.
    """
    if not persona_id:
        return _PERSONAS["goku"]

    return _PERSONAS.get(persona_id, _PERSONAS["goku"])
