from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict

from app.db.session import get_db
from app.services.memory_service import (
    get_or_create_conversation,
    add_message,
    add_long_term_memory,
    get_context,
)

router = APIRouter(prefix="/memmory", tags=["Memory"])


# =========================
# Schemas
# =========================

class MemoryContextResponse(BaseModel):
    messages: List[Dict[str, str]]
    long_term: List[str]


class MessageWriteRequest(BaseModel):
    user_id: str
    persona_id: str
    role: str          # user | assistant | system
    content: str
    long_term: bool = False


# =========================
# Endpoints
# =========================

@router.get(
    "/context",
    response_model=MemoryContextResponse,
)
def read_context(
    user_id: str,
    persona_id: str,
    db: Session = Depends(get_db),
):
    """
    Fetch short-term conversation + long-term memory.
    """
    return get_context(
        db=db,
        user_id=user_id,
        persona_id=persona_id,
    )


@router.post("/write")
def write_memory(
    payload: MessageWriteRequest,
    db: Session = Depends(get_db),
):
    """
    Store a message in conversation memory.
    Optionally store it as long-term memory.
    """
    conversation = get_or_create_conversation(
        db=db,
        user_id=payload.user_id,
        persona_id=payload.persona_id,
    )

    add_message(
        db=db,
        conversation_id=conversation.id,
        role=payload.role,
        content=payload.content,
    )

    if payload.long_term:
        add_long_term_memory(
            db=db,
            user_id=payload.user_id,
            persona_id=payload.persona_id,
            content=payload.content,
        )

    return {"status": "stored"}
