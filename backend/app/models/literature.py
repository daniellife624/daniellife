from sqlalchemy import Column, Integer, String, Text
from ..database import Base


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(String(10), nullable=False)
    grade = Column(String(50), nullable=False)
    award = Column(String(200), nullable=False)
    result = Column(String(100), nullable=False)


class LiteratureWork(Base):
    __tablename__ = "literature_works"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    year = Column(String(10), nullable=False)
    award = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    excerpt = Column(Text, nullable=False)
    full_text = Column(Text, nullable=False)
