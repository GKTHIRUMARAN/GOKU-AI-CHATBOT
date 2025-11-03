import os, requests
from dotenv import load_dotenv
from backend.utils.file_utils import read_file_safe

load_dotenv()
LM_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
MODEL = os.getenv("MODEL_NAME", "Llama-3-8B-Instruct")

class MemoryManager:
    def __init__(self, memory_path="characters/goku/memory.txt", limit=15):
        self.memory_path = memory_path
        self.limit = limit

    def count_lines(self):
        return sum(1 for _ in open(self.memory_path, "r", encoding="utf-8")) if os.path.exists(self.memory_path) else 0

    def summarize(self):
        """Summarize last N lines if file too long."""
        if not os.path.exists(self.memory_path):
            return
        with open(self.memory_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) <= self.limit:
            return  # nothing to condense

        text_chunk = "".join(lines[-self.limit:])
        prompt = f"Summarize this conversation in 3 sentences keeping key facts:\n{text_chunk}"

        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150,
            "temperature": 0.5,
        }

        try:
            res = requests.post(LM_URL, json=payload, timeout=25)
            res.raise_for_status()
            summary = res.json()["choices"][0]["message"]["content"].strip()

            with open(self.memory_path, "w", encoding="utf-8") as f:
                f.write(f"[Summary Memory]\n{summary}\n")
        except Exception:
            pass  # fail silently if LM Studio busy
