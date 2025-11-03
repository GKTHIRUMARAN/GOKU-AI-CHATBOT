from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import chat

app = FastAPI(title="Project Z - Goku AI Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"msg": "Goku AI Backend Active"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(chat.router, prefix="/api")
