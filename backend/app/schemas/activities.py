from typing import Optional
from pydantic import BaseModel


class ExperienceOut(BaseModel):
    id: int
    type: str
    title: str
    organization: str
    period: str                         # "YYYY/MM – YYYY/MM" computed from dates
    startDate: Optional[str] = None     # ISO "YYYY-MM-DD"
    endDate: Optional[str] = None
    contribution: str
    photos: list[str] = []


class ExperienceIn(BaseModel):
    type: str
    title: str
    organization: str
    period: str                         # "YYYY/MM – YYYY/MM" — parsed server-side
    contribution: str
    photos: list[str] = []


class TravelEntryOut(BaseModel):
    id: int
    country: str
    city: str
    continent: str
    visitedAt: str                      # ISO "YYYY-MM-DD"
    journal: Optional[str] = None
    companions: Optional[str] = None
    activities: Optional[str] = None
    purchases: Optional[str] = None
    photos: list[str] = []


class TravelEntryIn(BaseModel):
    country: str
    city: str
    continent: str
    visitedAt: str                      # ISO "YYYY-MM-DD"
    journal: Optional[str] = None
    companions: Optional[str] = None
    activities: Optional[str] = None
    purchases: Optional[str] = None
    photos: list[str] = []
