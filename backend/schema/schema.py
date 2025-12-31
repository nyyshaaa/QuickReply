from typing import Optional, List
from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Text, func, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from uuid6 import uuid7

class Conversations(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    
    session_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            nullable=False,
            unique=True,
            index=True,
        ),
        default_factory=uuid7,
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(), 
        )
    )

    messages: List["Messages"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

class Messages(SQLModel, table=True):
   

    id: Optional[int] = Field(default=None, primary_key=True)

    conversation_id: int = Field(
        foreign_key="conversations.id",
        index=True,
        nullable=False,
    )

    sender: str = Field(
        sa_column=Column(
            Enum("user", "ai", "system", name="message_sender"),
            nullable=False,
        )
    )

    text: str = Field(
        sa_column=Column(Text, nullable=False)
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        )
    )

    conversation: Optional[Conversations] = Relationship(back_populates="messages")



