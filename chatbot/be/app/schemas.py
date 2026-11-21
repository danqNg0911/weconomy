from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ThreadCreate(BaseModel):
    id: UUID | None = None
    title: str = Field(default="New chat", min_length=1, max_length=200)


class ThreadPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    archived: bool | None = None


class ThreadTitle(BaseModel):
    content: str = Field(min_length=1, max_length=20000)


class ThreadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID | None
    title: str
    archived: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def utc_timestamps(cls, value):
        return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


class MessageCreate(BaseModel):
    # assistant-ui IDs may not be UUIDs; the server maps them deterministically.
    id: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=20000)
    parent_id: str | None = Field(default=None, max_length=200)

    @field_validator("content")
    @classmethod
    def nonempty(cls, value):
        if not value.strip():
            raise ValueError("Message must not be blank")
        return value


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    thread_id: UUID
    role: Literal["user", "assistant"]
    content: str
    details: dict
    status: Literal["pending", "completed", "failed"]
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def utc_timestamp(cls, value):
        return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value
