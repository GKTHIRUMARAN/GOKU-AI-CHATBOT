from typing import List, Dict


def build_memory_grounding_prompt(
    long_term_memory: List[str],
) -> str:
    """
    Convert long-term memory facts into a grounding system prompt.
    Memory must influence reasoning, not be repeated verbatim.
    """

    if not long_term_memory:
        return ""

    memory_lines = "\n".join(
        f"- {fact}" for fact in long_term_memory
    )

    return f"""
You have access to the following long-term information about the user.
Use this information only when it is relevant to the user's request.
Do not explicitly mention that you are using memory unless the user asks.
Do not fabricate details beyond what is listed.

Known user information:
{memory_lines}
""".strip()
