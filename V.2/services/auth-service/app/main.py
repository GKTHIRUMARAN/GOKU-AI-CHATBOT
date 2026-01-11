from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.v1.auth import router as auth_router
from app.db.session import get_db

app = FastAPI(
    title="Goku AI v3 - Auth Service",
    version="1.0.0",
    description="Authentication service for Goku AI v3",
)

# --------------------------------------------------
# CORS CONFIGURATION (FRONTEND REQUIRED)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend (Next.js)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Health probes
# --------------------------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "auth-service",
        "version": "1.0.0",
    }


@app.get("/ready", tags=["Health"])
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness probe:
    - Confirms database connectivity
    """
    try:
        db.execute(text("SELECT 1"))
        db.commit()
        return {
            "status": "ready",
            "service": "auth-service",
        }
    except Exception as e:
        return {
            "status": "not-ready",
            "service": "auth-service",
            "error": str(e),
        }

# --------------------------------------------------
# Routes
# --------------------------------------------------
app.include_router(auth_router)