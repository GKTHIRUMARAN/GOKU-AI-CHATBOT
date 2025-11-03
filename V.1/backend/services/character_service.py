'''
import os
from backend.utils.file_utils import read_file_safe, write_to_memory, get_character_paths

class CharacterService:
    def __init__(self, base_dir="characters"):
        self.base_dir = base_dir
        self.paths = get_character_paths(self.base_dir, "goku")

    def load_character_data(self):
        """Return prompt, knowledge, memory for Goku."""
        prompt = read_file_safe(self.paths["prompt"])
        knowledge = read_file_safe(self.paths["knowledge"])
        memory = read_file_safe(self.paths["memory"])
        return {"prompt": prompt, "knowledge": knowledge, "memory": memory}

    def update_memory(self, user_msg: str, ai_reply: str):
        """Append conversation to memory.txt."""
        write_to_memory(self.paths["memory"], user_msg, ai_reply)
'''
import os
from backend.utils.file_utils import read_file_safe, get_character_paths

class CharacterService:
    def __init__(self, base_dir="characters"):
        self.base_dir = base_dir
        self.paths = get_character_paths(self.base_dir, "goku")

    def load_character_data(self):
        prompt = read_file_safe(self.paths["prompt"])
        knowledge = read_file_safe(self.paths["knowledge"])
        memory = read_file_safe(self.paths["memory"])
        return {"prompt": prompt, "knowledge": knowledge, "memory": memory}

    def update_memory(self, text: str):
        with open(self.paths["memory"], "a", encoding="utf-8") as f:
            f.write(f"\n{text}\n")
