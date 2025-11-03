# app.py -- Goku RAG chatbot (LM Studio backend) + Gradio UI
import os
import json
import time
import pickle
from pathlib import Path

import requests
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import gradio as gr

# ----------------------------
# CONFIG - edit these values
# ----------------------------
PROJECT_DIR = Path.cwd()
PROMPT_FILE = PROJECT_DIR / "prompt.txt"
KNOWLEDGE_FILE = PROJECT_DIR / "knowledge.txt"
MEMORY_FILE = PROJECT_DIR / "memory.txt"

# LM Studio settings - change to match your setup
LM_STUDIO_BASE_URL = os.environ.get("LM_STUDIO_URL", "http://192.168.57.241:1234") #"http://192.168.20.241:1234")  # set to your LM Studio server URL
LM_STUDIO_MODEL = os.environ.get("LM_STUDIO_MODEL", "meta-llama-3-8b-instruct")     # set the model name exactly as LM Studio shows
LM_STUDIO_API_KEY = os.environ.get("LM_STUDIO_API_KEY", None)                 # optional

# Retrieval + embeddings settings
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"   # sentence-transformers model (small, fast)
EMBED_CACHE = PROJECT_DIR / "embed_cache.pkl"
CHUNK_SIZE = 800         # chars per chunk (rough)
CHUNK_OVERLAP = 150
TOP_K = 6                # how many knowledge chunks to retrieve
MAX_MEMORY_CHARS = 5000  # how many chars of memory to include in prompt

# Generation settings
MAX_TOKENS = 512
TEMPERATURE = 0.7

# ----------------------------
# Utilities
# ----------------------------
def read_file(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""

def write_file_append(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def chunk_text(text: str, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    text = text.replace("\r\n", "\n")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for p in paragraphs:
        while len(p) > size:
            cut = p[:size]
            last_space = cut.rfind(" ")
            if last_space <= 0:
                last_space = size
            chunk = p[:last_space].strip()
            chunks.append(chunk)
            p = p[last_space - overlap:].strip()
        if p:
            chunks.append(p)
    # fallback if nothing split
    if not chunks and text:
        for i in range(0, len(text), size - overlap):
            chunks.append(text[i:i+size])
    return chunks

# ----------------------------
# Embeddings & Retrieval
# ----------------------------
class Retriever:
    def __init__(self, kb_path: Path, model_name=EMBED_MODEL_NAME, cache_path=EMBED_CACHE):
        self.kb_path = kb_path
        self.cache_path = cache_path
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.embeddings = None
        self.nn = None
        self._load_or_build()

    def _load_or_build(self):
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "rb") as f:
                    saved = pickle.load(f)
                if saved.get("kb_mtime") == os.path.getmtime(self.kb_path):
                    self.chunks = saved["chunks"]
                    self.embeddings = saved["embeddings"]
                    self.nn = NearestNeighbors(metric="cosine")
                    self.nn.fit(self.embeddings)
                    return
            except Exception:
                pass
        # build fresh
        text = read_file(self.kb_path)
        if not text:
            self.chunks = []
            self.embeddings = np.zeros((0, self.model.get_sentence_embedding_dimension()))
            self.nn = None
            return
        self.chunks = chunk_text(text)
        self.embeddings = self.model.encode(self.chunks, show_progress_bar=True, convert_to_numpy=True)
        self.nn = NearestNeighbors(n_neighbors=min(10, len(self.embeddings)), metric="cosine")
        self.nn.fit(self.embeddings)
        saved = {
            "kb_mtime": os.path.getmtime(self.kb_path),
            "chunks": self.chunks,
            "embeddings": self.embeddings
        }
        with open(self.cache_path, "wb") as f:
            pickle.dump(saved, f)

    def retrieve(self, query: str, top_k=TOP_K):
        if not self.chunks:
            return []
        q_emb = self.model.encode([query], convert_to_numpy=True)
        dists, idxs = self.nn.kneighbors(q_emb, n_neighbors=min(top_k, len(self.chunks)))
        idxs = idxs[0]
        return [self.chunks[i] for i in idxs]

# ----------------------------
# LM Studio call (OpenAI-like)
# ----------------------------
def call_lm_studio(messages, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
    url = LM_STUDIO_BASE_URL.rstrip("/") + "/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    if LM_STUDIO_API_KEY:
        headers["Authorization"] = f"Bearer {LM_STUDIO_API_KEY}"
    payload = {
        "model": LM_STUDIO_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=120)
    resp.raise_for_status()
    out = resp.json()
    # Typical OpenAI-like response: choices[0].message.content
    try:
        return out["choices"][0]["message"]["content"]
    except Exception:
        # fallback to text
        try:
            return out["choices"][0].get("text", "")
        except Exception:
            return json.dumps(out)

# ----------------------------
# Memory helpers
# ----------------------------
def get_recent_memory(max_chars=MAX_MEMORY_CHARS):
    text = read_file(MEMORY_FILE)
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    # return last chunk
    return text[-max_chars:]

def append_memory(user_msg, assistant_msg):
    entry = f"User: {user_msg}\nGoku: {assistant_msg}\n"
    write_file_append(MEMORY_FILE, entry)

def clear_memory():
    open(MEMORY_FILE, "w", encoding="utf-8").close()

# ----------------------------
# High-level generate
# ----------------------------
retriever = Retriever(KNOWLEDGE_FILE)

def generate_reply(user_input: str):
    system_prompt = read_file(PROMPT_FILE).strip() or "You are Son Goku. Stay in-character."
    recent_mem = get_recent_memory()
    retrieved = retriever.retrieve(user_input, top_k=TOP_K)
    retrieved_text = "\n\n".join(retrieved) if retrieved else "No relevant knowledge found."

    # Compose user content (keeps system prompt clean)
    user_content = (
        f"Conversation memory (most recent):\n{recent_mem}\n\n"
        f"Relevant knowledge (retrieved):\n{retrieved_text}\n\n"
        f"User: {user_input}\n\nRespond in-character as Son Goku. Keep it natural and concise."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    assistant_text = call_lm_studio(messages)
    assistant_text = assistant_text.strip()
    # persist memory
    append_memory(user_input, assistant_text)
    return assistant_text

# ----------------------------
# Gradio UI
# ----------------------------
def respond(user_message, chat_history):
    reply = generate_reply(user_message)
    chat_history = chat_history or []
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": reply})
    return chat_history, ""

def reset_chat():
    return []

def do_clear_memory():
    clear_memory()
    return gr.update(value="Memory cleared.")

with gr.Blocks(title="GokuAI Chatbot") as demo:
    gr.Markdown("## Goku persona style chatbot (LM Studio backend)")
    chatbot = gr.Chatbot(type="messages", height=500)
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Say something to Goku... (e.g. 'Hey Goku, how do you train?')")
        send = gr.Button("Send")
    with gr.Row():
        clear_chat_btn = gr.Button("Clear chat")
        clear_mem_btn = gr.Button("Clear memory")
    send.click(respond, [txt, chatbot], [chatbot, txt])
    txt.submit(respond, [txt, chatbot], [chatbot, txt])
    clear_chat_btn.click(reset_chat, [], chatbot)
    clear_mem_btn.click(do_clear_memory, [], None)
if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
