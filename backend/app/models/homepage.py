from sqlalchemy import Column, Integer, String, Text, Float
from ..database import Base


class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(200), nullable=False)
    department = Column(String(200), nullable=False)
    period = Column(String(100), nullable=False)
    contribution = Column(Text, nullable=False)
    photos = Column(Text, default="[]")        # JSON array of URLs


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    type = Column(String(20), nullable=False)  # finance | code | UIUX
    tech = Column(Text, default="[]")          # JSON array
    people = Column(Integer, default=1)
    summary = Column(Text, nullable=False)
    links = Column(Text, default="[]")         # JSON array


class CertItem(Base):
    __tablename__ = "cert_items"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(20), nullable=False)  # language | finance
    name = Column(String(200), nullable=False)
    level = Column(String(100), nullable=True)
    progress = Column(Integer, default=0)


class AcademicMilestone(Base):
    __tablename__ = "academic_milestones"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(200), nullable=False)
    sublabel = Column(String(200), nullable=False)
    year = Column(String(10), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)


class FuturePlan(Base):
    __tablename__ = "future_plans"

    id = Column(Integer, primary_key=True, index=True)
    horizon = Column(String(20), nullable=False)  # short | mid-short | mid
    content = Column(Text, nullable=False)
    order = Column(Integer, default=0)
