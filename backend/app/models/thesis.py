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
    content = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending | approved | rejected
    created_at = Column(DateTime, server_default=func.now())


class ThesisPaper(Base):
    __tablename__ = "thesis_papers"

    id = Column(Integer, primary_key=True, index=True)
    authors = Column(String(500), nullable=False)
    year = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    journal = Column(String(300), nullable=False)
    purpose = Column(Text, nullable=False)
    contribution = Column(Text, nullable=False)
    topics = Column(Text, default="[]")            # JSON array
