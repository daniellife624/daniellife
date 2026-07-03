from sqlalchemy import Column, Integer, String, Text, Float, Date
from ..database import Base


class Internship(Base):
    __tablename__ = "internships"
    id           = Column(Integer, primary_key=True)
    company      = Column(String(200), nullable=False)
    dept         = Column(String(200), nullable=False, default="")
    role         = Column(String(100), nullable=False, default="實習生")
    start_date   = Column(Date, nullable=True)
    end_date     = Column(Date, nullable=True)
    contribution = Column(Text, nullable=False)
    photo_url    = Column(String(500), nullable=True)


class Project(Base):
    __tablename__ = "projects"
    id          = Column(Integer, primary_key=True)
    name        = Column(String(200), nullable=False)
    type        = Column(String(20), nullable=False)   # comma-separated subset of code|uiux|finance
    tech_label  = Column(String(100), nullable=False, default="主要職責")
    tech        = Column(String(500), nullable=False, default="")
    members     = Column(Integer, default=1)
    period      = Column(String(50), nullable=False, default="")
    core        = Column(String(200), nullable=False, default="")
    github_url  = Column(String(500), nullable=True)
    youtube_url = Column(String(500), nullable=True)
    other_url   = Column(String(500), nullable=True)
    star        = Column(Text, default="[]")           # JSON: [{label, text}, ...]
    created_at  = Column(String(20), nullable=False, default="")


class LanguageCert(Base):
    __tablename__ = "language_certs"
    id    = Column(Integer, primary_key=True)
    lang  = Column(String(10), nullable=False)          # 'en' | 'jp'
    name  = Column(String(100), nullable=False)
    score = Column(String(50), nullable=False)
    pct   = Column(Float, nullable=False, default=0.0)


class CertGroup(Base):
    __tablename__ = "cert_groups"
    id         = Column(Integer, primary_key=True)
    domain     = Column(String(20), nullable=False)     # 'finance' | 'it'
    category   = Column(String(100), nullable=False)
    items      = Column(Text, default="[]")             # JSON: list[str]
    sort_order = Column(Integer, default=0)


class AcademicMilestone(Base):
    __tablename__ = "academic_milestones"
    id         = Column(Integer, primary_key=True)
    school     = Column(String(200), nullable=False)
    major      = Column(String(200), nullable=False)
    period     = Column(String(50), nullable=False)
    gpa        = Column(String(50), nullable=False, default="")
    rank       = Column(String(50), nullable=False, default="")
    facts      = Column(Text, default="[]")             # JSON: list[str]
    sort_order = Column(Integer, default=0)


class FuturePlan(Base):
    __tablename__ = "future_plans"
    id         = Column(Integer, primary_key=True)
    phase      = Column(String(20), nullable=False)     # short | mid-short | mid
    title      = Column(String(100), nullable=False)
    subtitle   = Column(String(200), nullable=False)
    items      = Column(Text, default="[]")             # JSON: list[str]
    sort_order = Column(Integer, default=0)
