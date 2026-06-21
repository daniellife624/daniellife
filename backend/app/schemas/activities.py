import re
from typing import Optional
from pydantic import BaseModel, field_validator


_PERIOD_RE = re.compile(r'^\d{4}/(0[1-9]|1[0-2]) – (\d{4}/(0[1-9]|1[0-2])|至今)$')
_DATE_RE = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$')
_CONTINENTS = {'Asia', 'Europe', 'Americas', 'Africa', 'Australia'}


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

    @field_validator('type')
    @classmethod
    def type_choices(cls, v: str) -> str:
        if v not in ('leadership', 'club'):
            raise ValueError('「類型」須為 leadership 或 club')
        return v

    @field_validator('title', 'organization', 'contribution')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('period')
    @classmethod
    def period_format(cls, v: str) -> str:
        if not _PERIOD_RE.match(v.strip()):
            raise ValueError('「期間」格式須為 YYYY/MM – YYYY/MM 或 YYYY/MM – 至今')
        return v.strip()


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

    @field_validator('country', 'city')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('continent')
    @classmethod
    def continent_choices(cls, v: str) -> str:
        if v not in _CONTINENTS:
            raise ValueError('「洲別」須為 Asia / Europe / Americas / Africa / Australia')
        return v

    @field_validator('visitedAt')
    @classmethod
    def visited_at_format(cls, v: str) -> str:
        if not _DATE_RE.match(v.strip()):
            raise ValueError('「造訪日期」格式須為 YYYY-MM-DD')
        return v.strip()
