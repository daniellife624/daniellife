import re
from typing import Optional
from pydantic import BaseModel, field_validator


_PERIOD_RE = re.compile(r'^\d{4}[./]\d{2}$')
_DATE_RE = re.compile(r'^\d{4}[./\-](0[1-9]|1[0-2])[./\-](0[1-9]|[12]\d|3[01])$')


class LiteratureWorkOut(BaseModel):
    id: int
    title: str
    ageWritten: Optional[int] = None
    period: Optional[str] = None        # "YYYY.MM"，頒發日期
    issuer: Optional[str] = None        # 頒發單位
    category: Optional[str] = None      # 小說 / 散文 / 新詩
    awards: str = ""
    summary: str
    fullText: Optional[str] = None


class LiteratureWorkIn(BaseModel):
    title: str
    ageWritten: Optional[int] = None
    period: Optional[str] = None        # "YYYY-MM" or "YYYY.MM" — parsed server-side
    issuer: Optional[str] = None
    category: Optional[str] = None
    awards: str = ""
    summary: str
    fullText: Optional[str] = None

    @field_validator('title', 'summary')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('ageWritten')
    @classmethod
    def age_positive(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 1:
            raise ValueError('「撰寫年齡」須為正整數')
        return v

    @field_validator('period')
    @classmethod
    def period_format(cls, v: Optional[str]) -> Optional[str]:
        if v and not _PERIOD_RE.match(v.strip()):
            raise ValueError('「頒發日期」格式須為 YYYY.MM 或 YYYY/MM')
        return v.strip() if v else None

    @field_validator('category')
    @classmethod
    def category_choices(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ('小說', '散文', '新詩'):
            raise ValueError('「分類標籤」須為 小說 / 散文 / 新詩')
        return v or None


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

    @field_validator('gradeLabel', 'awardTitle', 'result')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('date')
    @classmethod
    def date_format(cls, v: str) -> str:
        if not _DATE_RE.match(v.strip()):
            raise ValueError('「日期」格式須為 YYYY.MM.DD 或 YYYY-MM-DD')
        return v.strip()
