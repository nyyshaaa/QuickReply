

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schema.schema import Conversations, Messages


async def get_or_create_conversation(
    session: AsyncSession,
    session_id: str,
) -> dict[str, str | int]:
  
    stmt = (
        insert(Conversations)
        .values(session_id=session_id)
        .on_conflict_do_nothing(
            index_elements=["session_id"]
        )
        .returning(Conversations.id, Conversations.session_id)
    )
    result = await session.execute(stmt)
    row = result.one_or_none()
    if row is  None:
        result = await session.execute(
            select(Conversations.id,Conversations.session_id).where(
                Conversations.session_id == session_id
            )
        )
        row = result.one_or_none()

    if row is None:
        raise RuntimeError(
            "Conversation insert conflict but record not found"
        )
        
    return {"id": row[0], "session_id": row[1]}

    
async def record_message(
    session: AsyncSession,
    *,
    conversation_id: int,
    sender: str,
    input_message: str,
) -> None:
    session.add(
        Messages(
            conversation_id=conversation_id,
            sender=sender,
            text=input_message,
        )
    )

async def fetch_recent_history(
    session: AsyncSession,
    *,
    conversation_id: int,
    limit: int = 10,
) -> list[Messages]:
    stmt = select(Messages).where(
        Messages.conversation_id == conversation_id
        ).order_by(Messages.created_at.desc()).limit(limit)
    result = await session.execute(stmt)
    return list(reversed(result.scalars().all()))