import json
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator


class ThesisNoteOut(BaseModel):
    id: int
    content: str
    updatedAt: Optional[datetime] = None

    model_config = {"from_attributes": True, "populate_by_name": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "updated_at"):
            return cls(id=obj.id, content=obj.content, updatedAt=obj.updated_at)
        return super().model_validate(obj, **kwargs)


class ThesisNoteIn(BaseModel):
    content: str


class ThesisIdeaOut(BaseModel):
    id: int
    content: str
    status: str
    createdAt: Optional[datetime] = None

    model_config = {"from_attributes": True, "populate_by_name": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "created_at"):
            return cls(id=obj.id, content=obj.content, status=obj.status, createdAt=obj.created_at)
        return super().model_validate(obj, **kwargs)


class ThesisIdeaIn(BaseModel):
    content: str
    status: str = "pending"


class ThesisIdeaUpdate(BaseModel):
    status: str


class ThesisPaperOut(BaseModel):
    id: int
    authors: str
    year: int
    title: str
    journal: str
    purpose: str
    contribution: str
    topics: list[str] = []

    @field_validator("topics", mode="before")
    @classmethod
    def parse_topics(cls, v):
        return json.loads(v) if isinstance(v, str) else v

    model_config = {"from_attributes": True}


class ThesisPaperIn(BaseModel):
    authors: str
    year: int
    title: str
    journal: str
    purpose: str
    contribution: str
    topics: list[str] = []
