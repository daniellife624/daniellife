from typing import Optional
from pydantic import BaseModel


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
