from sqlalchemy import Column, Integer, String, Text, DateTime, func
from ..database import Base


class ThesisNote(Base):
    __tablename__ = "thesis_notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False, default="")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ThesisIdea(Base):
    __tablename__ = "thesis_ideas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, default="")
    content = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending | approved | rejected
    created_at = Column(DateTime, server_default=func.now())


class ThesisPaper(Base):
    __tablename__ = "thesis_papers"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(100), nullable=False, default="")   # single topic tag
    name = Column(Text, nullable=False)                       # paper title
    journal = Column(String(300), nullable=False)
    authors = Column(String(500), nullable=False)
    year = Column(Integer, nullable=False)
    purpose = Column(Text, nullable=False)
    contribution = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)                       # HTML content, may embed <img> tags
