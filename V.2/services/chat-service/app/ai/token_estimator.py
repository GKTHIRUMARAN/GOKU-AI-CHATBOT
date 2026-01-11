from typing import List, Dict


# -----------------------------
# Generic helpers
# -----------------------------

def rough_token_count(text: str) -> int:
    """
    Very safe approximation:
    1 token ≈ 4 characters (industry standard rough rule)
    """
    if not text:
        return 0
    return max(1, len(text) // 4)


def count_messages(messages: List[Dict[str, str]]) -> int:
    total = 0
    for m in messages:
        total += rough_token_count(m.get("content", ""))
    return total


# -----------------------------
# Engine-specific estimators
# -----------------------------

def estimate_gemini_tokens(
    persona_prompt: str,
    long_term_memory: List[str],
    conversation_messages: List[Dict[str, str]],
    user_message: str,
    estimated_output_tokens: int = 256,
) -> int:
    """
    Gemini input + expected output tokens
    """

    input_tokens = 0

    # System / persona
    input_tokens += rough_token_count(persona_prompt)

    # Long-term memory
    for mem in long_term_memory:
        input_tokens += rough_token_count(mem)

    # Conversation context
    input_tokens += count_messages(conversation_messages)

    # User message
    input_tokens += rough_token_count(user_message)

    return input_tokens + estimated_output_tokens


def estimate_local_tokens(
    persona_prompt: str,
    conversation_messages: List[Dict[str, str]],
    user_message: str,
) -> int:
    """
    Local engine does not need strict billing,
    but we still estimate for consistency.
    """
    tokens = rough_token_count(persona_prompt)
    tokens += count_messages(conversation_messages)
    tokens += rough_token_count(user_message)
    return tokens
