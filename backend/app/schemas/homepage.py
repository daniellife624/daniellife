import re
from typing import Optional
from pydantic import BaseModel, field_validator


_MONTH_RE = re.compile(r'^\d{4}/(0[1-9]|1[0-2])$')


class SortOrderItem(BaseModel):
    id: int
    sortOrder: int
_PERIOD_RE = re.compile(r'^\d{4}/(0[1-9]|1[0-2]) – (\d{4}/(0[1-9]|1[0-2])|至今)$')
_YEAR_PERIOD_RE = re.compile(r'^\d{4}(/\d{2})? – (\d{4}(/\d{2})?|至今)$')
_DATE_RE = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$')


# ── Internship ───────────────────────────────────────────────────
class InternshipOut(BaseModel):
    id: int
    company: str
    dept: str
    role: str
    period: str
    contribution: str
    photoUrl: Optional[str] = None

    model_config = {"from_attributes": True}


class InternshipIn(BaseModel):
    company: str
    dept: str
    role: str = "實習生"
    period: str = ""           # "YYYY/MM – YYYY/MM" — parsed server-side
    contribution: str
    photoUrl: Optional[str] = None

    @field_validator('company', 'dept', 'contribution')
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


# ── Project ──────────────────────────────────────────────────────
class StarItemOut(BaseModel):
    label: str
    text: str


class ProjectOut(BaseModel):
    id: int
    name: str
    type: str
    techLabel: str
    tech: str
    members: int
    period: str
    core: str
    githubUrl: Optional[str] = None
    youtubeUrl: Optional[str] = None
    star: list[StarItemOut] = []
    createdAt: str


class ProjectIn(BaseModel):
    name: str
    type: str
    techLabel: str = "使用技術"
    tech: str = ""
    members: int = 1
    period: str = ""
    core: str = ""
    githubUrl: Optional[str] = None
    youtubeUrl: Optional[str] = None
    star: list[StarItemOut] = []
    createdAt: str = ""

    @field_validator('name', 'core')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('type')
    @classmethod
    def type_choices(cls, v: str) -> str:
        if v not in ('code', 'uiux', 'finance'):
            raise ValueError('「type」須為 code / uiux / finance')
        return v

    @field_validator('members')
    @classmethod
    def members_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError('「成員人數」須為正整數')
        return v

    @field_validator('period')
    @classmethod
    def period_format(cls, v: str) -> str:
        if not _PERIOD_RE.match(v.strip()):
            raise ValueError('「期間」格式須為 YYYY/MM – YYYY/MM 或 YYYY/MM – 至今')
        return v.strip()

    @field_validator('createdAt')
    @classmethod
    def created_at_format(cls, v: str) -> str:
        if v and not _DATE_RE.match(v.strip()):
            raise ValueError('「建立日期」格式須為 YYYY-MM-DD')
        return v.strip()


# ── CertData (public read) ────────────────────────────────────────
class LangCertOut(BaseModel):
    name: str
    score: str
    pct: float


class CertGroupOut(BaseModel):
    category: str
    items: list[str] = []


class LanguageData(BaseModel):
    en: list[LangCertOut]
    jp: list[LangCertOut]


class CertDataOut(BaseModel):
    language: LanguageData
    finance: list[CertGroupOut]
    it: list[CertGroupOut]


# ── CertData (admin CRUD) ─────────────────────────────────────────
class LangCertAdminOut(BaseModel):
    id: int
    lang: str
    name: str
    score: str
    pct: float


class LangCertIn(BaseModel):
    lang: str            # 'en' | 'jp'
    name: str
    score: str
    pct: float = 0.0

    @field_validator('lang')
    @classmethod
    def lang_choices(cls, v: str) -> str:
        if v not in ('en', 'jp'):
            raise ValueError('「語言」須為 en 或 jp')
        return v

    @field_validator('name', 'score')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('pct')
    @classmethod
    def pct_range(cls, v: float) -> float:
        if not (0 <= v <= 100):
            raise ValueError('「進度百分比」須介於 0 到 100')
        return v


class CertGroupAdminOut(BaseModel):
    id: int
    domain: str          # 'finance' | 'it'
    category: str
    items: list[str] = []
    sortOrder: int = 0


class CertGroupIn(BaseModel):
    domain: str
    category: str
    items: list[str] = []
    sortOrder: int = 0

    @field_validator('domain')
    @classmethod
    def domain_choices(cls, v: str) -> str:
        if v not in ('finance', 'it', '財會', '資訊'):
            raise ValueError('「領域」須為 財會 或 資訊')
        return v

    @field_validator('category')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('「類別」不可空白')
        return v

    @field_validator('items')
    @classmethod
    def items_not_empty(cls, v: list) -> list:
        if not v:
            raise ValueError('「證照項目」至少要有一條')
        return v


# ── AcademicMilestone ────────────────────────────────────────────
class AcademicMilestoneOut(BaseModel):
    id: int
    school: str
    major: str
    period: str
    gpa: str
    rank: str
    facts: list[str] = []
    sortOrder: int = 0


class AcademicMilestoneIn(BaseModel):
    school: str
    major: str
    period: str
    gpa: str = ""
    rank: str = ""
    facts: list[str] = []
    sortOrder: int = 0

    @field_validator('school', 'major')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('period')
    @classmethod
    def period_format(cls, v: str) -> str:
        if not _YEAR_PERIOD_RE.match(v.strip()):
            raise ValueError('「期間」格式須為 YYYY – YYYY 或 YYYY – 至今')
        return v.strip()


# ── FuturePlan ───────────────────────────────────────────────────
class FuturePlanOut(BaseModel):
    id: int
    phase: str
    title: str
    subtitle: str
    items: list[str] = []
    sortOrder: int = 0


class FuturePlanIn(BaseModel):
    phase: str
    title: str
    subtitle: str
    items: list[str] = []
    sortOrder: int = 0

    @field_validator('phase')
    @classmethod
    def phase_choices(cls, v: str) -> str:
        if v not in ('short', 'mid-short', 'mid'):
            raise ValueError('「階段」須為 short / mid-short / mid')
        return v

    @field_validator('title', 'subtitle')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v
