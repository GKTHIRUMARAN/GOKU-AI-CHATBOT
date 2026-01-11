from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.core.config import get_settings

from app.clients.billing_client import (
    BillingServiceClient,
    BillingLimitExceeded,
)
from app.clients.memory_client import MemoryServiceClient

from app.memory.extractor import extract_long_term_memory
from app.memory.grounding import build_memory_grounding_prompt

from app.ai.router import get_ai_engine
from app.ai.token_estimator import (
    estimate_gemini_tokens,
    estimate_local_tokens,
)

from app.personas.registry import get_persona

router = APIRouter()

settings = get_settings()
billing = BillingServiceClient()
memory = MemoryServiceClient()


@router.post("/chat")
def chat(
    message: str,
    persona: str = "goku",
    current_user: dict = Depends(get_current_user),
):
    # --------------------------------------------------
    # 1️⃣ Auth user (FAIL FAST)
    # --------------------------------------------------
    user_id = current_user.get("email")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication payload",
        )

    # --------------------------------------------------
    # 2️⃣ Persona resolution
    # --------------------------------------------------
    persona_obj = get_persona(persona)

    # --------------------------------------------------
    # 3️⃣ Fetch memory context (safe fallback)
    # --------------------------------------------------
    try:
        context = memory.get_context(
            user_id=user_id,
            persona_id=persona_obj.id,
        )
    except Exception:
        # Memory failure must NEVER block chat
        context = {
            "messages": [],
            "long_term": [],
        }

    # --------------------------------------------------
    # 4️⃣ Token estimation (TASK 14.6.3)
    # --------------------------------------------------
    if settings.AI_PROVIDER == "gemini":
        estimated_tokens = estimate_gemini_tokens(
            persona_prompt=persona_obj.system_prompt,
            long_term_memory=context.get("long_term", []),
            conversation_messages=context.get("messages", []),
            user_message=message,
            estimated_output_tokens=256,
        )
    else:
        estimated_tokens = estimate_local_tokens(
            persona_prompt=persona_obj.system_prompt,
            conversation_messages=context.get("messages", []),
            user_message=message,
        )

    # --------------------------------------------------
    # 5️⃣ HARD billing enforcement (authoritative)
    # --------------------------------------------------
    try:
        billing.record_usage(
            user_id=user_id,
            endpoint="chat",
            tokens=estimated_tokens,
        )
    except BillingLimitExceeded:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Billing limit exceeded",
        )

    # --------------------------------------------------
    # 6️⃣ AI execution (memory-aware, grounded)
    # --------------------------------------------------
    ai_engine = get_ai_engine()

    grounded_memory = build_memory_grounding_prompt(
        context.get("long_term", [])
    )

    reply = ai_engine.generate_reply(
        persona_prompt=persona_obj.system_prompt,
        long_term_memory=grounded_memory,
        conversation_messages=context.get("messages", []),
        user_message=message,
    )

    # --------------------------------------------------
    # 7️⃣ Persist USER message (best-effort)
    # --------------------------------------------------
    try:
        memory.store_message(
            user_id=user_id,
            persona_id=persona_obj.id,
            role="user",
            content=message,
        )
    except Exception:
        pass  # never block response

    # --------------------------------------------------
    # 8️⃣ Auto long-term memory extraction
    # --------------------------------------------------
    memory_candidate = extract_long_term_memory(message)
    if memory_candidate:
        try:
            memory.store_long_term_memory(
                user_id=user_id,
                persona_id=persona_obj.id,
                content=memory_candidate,
            )
        except Exception:
            pass

    # --------------------------------------------------
    # 9️⃣ Response
    # --------------------------------------------------
    return {
        "reply": reply,
        "persona": persona_obj.id,
    }
