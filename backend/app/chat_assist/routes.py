

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.chat_assist.models import ChatRequest
from backend.app.chat_assist.dependencies import normalize_chat_request
from backend.app.chat_assist.repository import fetch_recent_history, get_or_create_conversation, record_message
from backend.db.dependencies import get_session

chat_assit_router=APIRouter()

@chat_assit_router.post("/message")
async def post_chat_message(
    payload: ChatRequest = Depends(normalize_chat_request),
    session: AsyncSession = Depends(get_session),
):
   

    # ---- Get or create conversation (idempotent & concurrency/retries safe) ----
    conversation = await get_or_create_conversation(
        session=session,
        session_id=payload.session_id,
    )

    conversation_id = conversation["id"]

    # ---- Persist user message ----
    await record_message(session,conversation_id,sender="user",text=payload.message)

    await session.commit()

    # ---- Fetch recent history ----
    history = await fetch_recent_history(
        session,
        conversation_id
    )

    history_payload = [
        {"sender": m.sender, "text": m.text}
        for m in history
    ]

    

   
@chat_assit_router.get("/health")
async def health_check(request: Request,session: AsyncSession = Depends(get_session)):
    stmt = select(1)
    await session.execute(stmt)
    return {"status": "ok"}
    