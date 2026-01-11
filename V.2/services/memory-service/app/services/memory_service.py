from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import Conversation, Message, MemoryEntry

settings = get_settings()


def get_or_create_conversation(
    db: Session,
    user_id: str,
    persona_id: str,
) -> Conversation:
    """
    Fetch an existing conversation or create a new one.
    """
    convo = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id,
            Conversation.persona_id == persona_id,
        )
        .first()
    )

    if convo:
        return convo

    convo = Conversation(
        user_id=user_id,
        persona_id=persona_id,
    )
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return convo


def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
) -> Message:
    """
    Store a message in a conversation.
    """
    msg = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def add_long_term_memory(
    db: Session,
    user_id: str,
    persona_id: str,
    content: str,
) -> MemoryEntry:
    """
    Store a long-term memory entry.
    """
    entry = MemoryEntry(
        user_id=user_id,
        persona_id=persona_id,
        content=content,
        is_long_term=True,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_context(
    db: Session,
    user_id: str,
    persona_id: str,
) -> dict:
    """
    Retrieve short-term and long-term memory context.
    """
    # Short-term memory (recent messages)
    convo = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id,
            Conversation.persona_id == persona_id,
        )
        .first()
    )

    messages = []
    if convo:
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == convo.id)
            .order_by(Message.created_at.desc())
            .limit(settings.MAX_CONTEXT_MESSAGES)
            .all()
        )
        messages = list(reversed(messages))

    # Long-term memory
    long_term = (
        db.query(MemoryEntry)
        .filter(
            MemoryEntry.user_id == user_id,
            MemoryEntry.persona_id == persona_id,
            MemoryEntry.is_long_term.is_(True),
        )
        .order_by(MemoryEntry.created_at.desc())
        .limit(settings.MAX_LONG_TERM_ENTRIES)
        .all()
    )

    return {
        "messages": [
            {"role": m.role, "content": m.content} for m in messages
        ],
        "long_term": [e.content for e in long_term],
    }
