from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.chat import router as chat_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# --------------------------------------------------
# CORS (Frontend ↔ Backend)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Health
# --------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "chat-service",
        "version": settings.APP_VERSION,
    }

# --------------------------------------------------
# Routes
# --------------------------------------------------
app.include_router(chat_router)