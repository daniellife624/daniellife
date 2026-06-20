import json
from typing import Optional
from pydantic import BaseModel, field_validator


class ExperienceOut(BaseModel):
    id: int
    type: str
    title: str
    organization: str
    period: str
    contribution: str
    photos: list[str] = []

    @field_validator("photos", mode="before")
    @classmethod
    def parse_photos(cls, v):
        return json.loads(v) if isinstance(v, str) else v

    model_config = {"from_attributes": True}


class ExperienceIn(BaseModel):
    type: str
    title: str
    organization: str
    period: str
    contribution: str
    photos: list[str] = []


class TravelEntryOut(BaseModel):
    id: int
    country: str
    city: str
    continent: str
    visitedAt: str
    journal: Optional[str] = None
    companions: Optional[str] = None
    activities: Optional[str] = None
    purchases: Optional[str] = None
    photos: list[str] = []

    @field_validator("visitedAt", mode="before")
    @classmethod
    def map_visited_at(cls, v):
        return v

    @field_validator("photos", mode="before")
    @classmethod
    def parse_photos(cls, v):
        return json.loads(v) if isinstance(v, str) else v

    model_config = {"from_attributes": True, "populate_by_name": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "visited_at") and not hasattr(obj, "visitedAt"):
            obj.__dict__.setdefault("visitedAt", obj.visited_at)
        return super().model_validate(obj, **kwargs)


class TravelEntryIn(BaseModel):
    country: str
    city: str
    continent: str
    visitedAt: str
    journal: Optional[str] = None
    companions: Optional[str] = None
    activities: Optional[str] = None
    purchases: Optional[str] = None
    photos: list[str] = []
