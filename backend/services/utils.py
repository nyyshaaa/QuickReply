
from typing import Dict, List
import google.genai as genai
from backend.config.settings import config_settings
from backend.services.domain_knowledge import DOMAIN_KNOWLEDGE_PROMPT

class LLMError(Exception):
    """Raised for controlled LLM failures."""
    pass



def _build_prompt(
    history: List[Dict[str, str]],
    user_message: str,
) -> str:
    """
    Build a single prompt string:
    [domain prompt] + [recent history] + [current user message]
    """

    parts: list[str] = []

    # Domain knowledge
    parts.append(DOMAIN_KNOWLEDGE_PROMPT.strip())
    parts.append("\n\nConversation so far:\n")

    # Recent history
    for msg in history:
        role = "User" if msg["sender"] == "user" else "Agent"
        parts.append(f"{role}: {msg['text']}\n")

    # Current turn
    parts.append(f"User: {user_message}\n")
    parts.append("Agent:")

    return "".join(parts)
