import json
from typing import Optional
from pydantic import BaseModel, field_validator


class InternshipOut(BaseModel):
    id: int
    company: str
    department: str
    period: str
    contribution: str
    photos: list[str] = []

    @field_validator("photos", mode="before")
    @classmethod
    def parse_photos(cls, v):
        return json.loads(v) if isinstance(v, str) else v

    model_config = {"from_attributes": True}


class InternshipIn(BaseModel):
    company: str
    department: str
    period: str
    contribution: str
    photos: list[str] = []


class ProjectOut(BaseModel):
    id: int
    title: str
    type: str
    tech: list[str] = []
    people: int
    summary: str
    links: list[str] = []

    @field_validator("tech", "links", mode="before")
    @classmethod
    def parse_json(cls, v):
        return json.loads(v) if isinstance(v, str) else v

    model_config = {"from_attributes": True}


class ProjectIn(BaseModel):
    title: str
    type: str
    tech: list[str] = []
    people: int = 1
    summary: str
    links: list[str] = []


class CertItemOut(BaseModel):
    id: int
    category: str
    name: str
    level: Optional[str] = None
    progress: int

    model_config = {"from_attributes": True}


class CertItemIn(BaseModel):
    category: str
    name: str
    level: Optional[str] = None
    progress: int = 0


class AcademicMilestoneOut(BaseModel):
    id: int
    label: str
    sublabel: str
    year: str
    x: float
    y: float

    model_config = {"from_attributes": True}


class FuturePlanOut(BaseModel):
    id: int
    horizon: str
    content: str
    order: int

    model_config = {"from_attributes": True}
