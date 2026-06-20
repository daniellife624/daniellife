from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ThesisNoteOut(BaseModel):
    content: str
    updatedAt: Optional[str] = None

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_row(cls, obj):
        return cls(
            content=obj.content,
            updatedAt=obj.updated_at.strftime("%Y/%m/%d") if obj.updated_at else None,
        )


class ThesisNoteIn(BaseModel):
    content: str


class ThesisIdeaOut(BaseModel):
    id: int
    title: str
    content: str
    status: str
    createdAt: Optional[str] = None

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_row(cls, obj):
        return cls(
            id=obj.id, title=obj.title, content=obj.content, status=obj.status,
            createdAt=obj.created_at.strftime("%Y-%m-%d") if obj.created_at else None,
        )


class ThesisIdeaIn(BaseModel):
    title: str = ""
    content: str
    status: str = "pending"


class ThesisIdeaUpdate(BaseModel):
    status: str


class ThesisPaperOut(BaseModel):
    id: int
    topic: str
    name: str
    journal: str
    authors: str
    year: int
    purpose: str
    contribution: str

    model_config = {"from_attributes": True}


class ThesisPaperIn(BaseModel):
    topic: str = ""
    name: str
    journal: str
    authors: str
    year: int
    purpose: str
    contribution: str
