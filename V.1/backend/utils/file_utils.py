import os

def read_file_safe(file_path: str) -> str:
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def write_to_memory(file_path: str, user_msg: str, ai_reply: str):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\nUser: {user_msg}\nGoku: {ai_reply}\n")

def get_character_paths(base_dir: str, character: str) -> dict:
    char_dir = os.path.join(base_dir, character.lower())
    os.makedirs(char_dir, exist_ok=True)
    return {
        "memory": os.path.join(char_dir, "memory.txt"),
        "knowledge": os.path.join(char_dir, "knowledge.txt"),
        "prompt": os.path.join(char_dir, "prompt.txt"),
    }
