

from backend.app.chat_assist.models import ChatRequest


async def normalize_chat_request(
    payload: ChatRequest,
) -> ChatRequest:
    payload.message = payload.message.strip()
    return payload