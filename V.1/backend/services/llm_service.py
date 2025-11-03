import os
import requests
from dotenv import load_dotenv
from backend.services.character_service import CharacterService
from backend.services.memory_manager import MemoryManager
from backend.services.emotion_service import detect_emotion

load_dotenv()

LM_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
MODEL = os.getenv("MODEL_NAME", "meta-llama-3-8b-instruct")

class LLMService:
    def __init__(self):
        self.character_service = CharacterService()
        self.memory_manager = MemoryManager()   

    def build_context(self, user_input: str) -> str:
        """Combine prompt, knowledge, memory, and new message."""
        char_data = self.character_service.load_character_data()
        return (
            f"{char_data['prompt']}\n\n"
            f"---\nKnowledge:\n{char_data['knowledge']}\n\n"
            f"---\nMemory:\n{char_data['memory']}\n\n"
            f"User: {user_input}\nGoku:"
        )

    def generate_response(self, user_input: str):
        try:
            context_prompt = self.build_context(user_input)

            payload = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are Goku. Reply naturally and confidently in character."},
                    {"role": "user", "content": user_input},
                ],
                "max_tokens": 256,
                "temperature": 0.8,
                "stream": False,
            }

            res = requests.post(LM_URL, json=payload, timeout=60)
            if res.status_code == 200:
                data = res.json()
                reply = (
                    data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                    .strip()
                )
                if not reply:
                    reply = "[Empty reply from model]"
            # detect emotion + update memory
            emotion = detect_emotion(reply)
            self.character_service.update_memory(
                f"User: {user_input}\nGoku ({emotion}): {reply}"
            )

            # periodic summarization
            self.memory_manager.summarize()

            return f"{reply}  \n🧠 Emotion: *{emotion}*"

        except Exception as e:
            return f"[Mock Reply] Goku says: '{user_input}' echoed. ({e})"
