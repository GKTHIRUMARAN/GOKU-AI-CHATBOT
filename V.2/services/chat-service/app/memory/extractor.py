import re
from typing import Optional


# ----------------------------
# Patterns that indicate
# long-term, stable user facts
# ----------------------------
MEMORY_PATTERNS = [
    r"\bi am learning ([^.?!]+)",
    r"\bi am a?n? ([^.?!]+)",
    r"\bi work as ([^.?!]+)",
    r"\bi work at ([^.?!]+)",
    r"\bmy goal is ([^.?!]+)",
    r"\bi want to become ([^.?!]+)",
    r"\bi prefer ([^.?!]+)",
]


# ----------------------------
# Words that indicate
# temporary or non-memory input
# ----------------------------
BLACKLIST = {
    "help",
    "question",
    "how",
    "what",
    "why",
    "when",
    "today",
    "now",
    "explain",
    "tell me",
}


def extract_long_term_memory(message: str) -> Optional[str]:
    """
    Extract a single long-term memory fact from user input.

    Returns:
        - A normalized memory sentence (str)
        - None if input should NOT be stored
    """

    if not message:
        return None

    text = message.strip().lower()

    # ----------------------------------
    # Reject questions
    # ----------------------------------
    if "?" in text:
        return None

    # ----------------------------------
    # Reject very short or trivial input
    # ----------------------------------
    if len(text.split()) < 4:
        return None

    # ----------------------------------
    # Reject blacklisted temporary intent
    # ----------------------------------
    for word in BLACKLIST:
        if word in text:
            return None

    # ----------------------------------
    # Pattern-based extraction
    # ----------------------------------
    for pattern in MEMORY_PATTERNS:
        match = re.search(pattern, text)
        if match:
            fact_body = match.group(1).strip()

            # Avoid ultra-generic memories
            if len(fact_body.split()) < 2:
                return None

            # Normalize memory sentence
            normalized = f"User {match.group(0).strip()}."
            return normalized.capitalize()

    return None