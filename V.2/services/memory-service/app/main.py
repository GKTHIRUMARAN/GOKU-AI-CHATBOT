from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.memory import router as memory_router

app = FastAPI(
    title="Goku AI v3 - Memory Service",
    version="1.0.0",
)

# --------------------------------------------------
# CORS (Frontend ↔ Backend)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Routes
# --------------------------------------------------
app.include_router(memory_router, prefix="/api/v1")

# --------------------------------------------------
# Health
# --------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "memory-service",
        "version": "1.0.0",
    }