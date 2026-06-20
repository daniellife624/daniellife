from typing import Optional
from pydantic import BaseModel


class LiteratureWorkOut(BaseModel):
    id: int
    title: str
    ageWritten: Optional[int] = None
    period: Optional[str] = None        # "YYYY.MM"
    awards: str = ""
    summary: str
    fullText: Optional[str] = None


class LiteratureWorkIn(BaseModel):
    title: str
    ageWritten: Optional[int] = None
    period: Optional[str] = None        # "YYYY-MM" or "YYYY.MM" — parsed server-side
    awards: str = ""
    summary: str
    fullText: Optional[str] = None


class TimelineEventOut(BaseModel):
    id: int
    gradeLabel: str
    awardTitle: str
    result: str
    date: str                           # "YYYY.MM.DD"
    workId: Optional[int] = None


class TimelineEventIn(BaseModel):
    gradeLabel: str
    awardTitle: str
    result: str
    date: str                           # "YYYY-MM-DD" or "YYYY.MM.DD"
    workId: Optional[int] = None
