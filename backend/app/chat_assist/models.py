from pydantic import BaseModel, Field
from uuid import UUID

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1500)
    sessionId: UUID   