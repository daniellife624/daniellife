from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator


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

    @field_validator('content')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('「筆記內容」不可空白')
        return v


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

    @field_validator('content')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('「內容」不可空白')
        return v

    @field_validator('status')
    @classmethod
    def status_choices(cls, v: str) -> str:
        if v not in ('pending', 'approved', 'rejected'):
            raise ValueError('「狀態」須為 pending / approved / rejected')
        return v


class ThesisIdeaUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None

    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError('「內容」不可空白')
        return v

    @field_validator('status')
    @classmethod
    def status_choices(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ('pending', 'approved', 'rejected'):
            raise ValueError('「狀態」須為 pending / approved / rejected')
        return v


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

    @field_validator('name', 'journal', 'authors', 'purpose', 'contribution')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('year')
    @classmethod
    def year_valid(cls, v: int) -> int:
        if not (1900 <= v <= 2100):
            raise ValueError('「年份」須為合理的西元年（1900–2100）')
        return v
