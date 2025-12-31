
from typing import List, Dict

from backend.services.utils import LLMError, _build_prompt
from backend.services.__init__ import _gem_client,_gem_model


async def generate_agent_reply(
    *,
    history: List[Dict[str, str]],
    user_message: str,
) -> str:
    """
    Generates an AI reply using Gemini, conditioned on domain knowledge
    and recent conversation history.
    """

    prompt = _build_prompt(history, user_message)

    try:
        response = _gem_client.models.generate_content(
            model = _gem_model,  
            contents = prompt,
        )

        if not response.text:
            raise LLMError("Empty response from LLM")

        return response.text.strip()

    except LLMError:
        raise

    # timeout , rate limit , invalid key , network error can be handled more specifcially by extra checks , 
    # for now we just log the exc in the outer handler with actual reason . 
    # catching here to re-raise so that they are not caught by fastapi error handlker without recording the error message .
    except Exception as exc:
        # unexpected provider / SDK / network issues
        raise LLMError("LLM service unavailable") from exc


