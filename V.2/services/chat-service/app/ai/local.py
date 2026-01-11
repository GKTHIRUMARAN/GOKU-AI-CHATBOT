from app.personas.base import Persona


class LocalAIEngine:
    def generate_reply(self, messages, persona: Persona, user_context: dict) -> str:
        user_msg = messages[-1]["content"]

        return (
            f"[GOKU MODE]\n"
            f"Hello {user_context['email']}.\n\n"
            f'You asked:\n"{user_msg}"\n\n'
            f"This is a local AI response used for development and testing."
        )
