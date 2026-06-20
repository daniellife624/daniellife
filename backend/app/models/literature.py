from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from ..database import Base


class LiteratureWork(Base):
    __tablename__ = "literature_works"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    age_written = Column(Integer, nullable=True)
    period      = Column(Date, nullable=True)       # stored as date, serialized to "YYYY.MM"
    awards      = Column(Text, nullable=False, default="")
    summary     = Column(Text, nullable=False)
    full_text   = Column(Text, nullable=True)


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id          = Column(Integer, primary_key=True, index=True)
    grade_label = Column(String(100), nullable=False)   # "小學 / 五年級"
    award_title = Column(String(200), nullable=False)
    result      = Column(String(100), nullable=False)
    date        = Column(Date, nullable=False)           # serialized to "YYYY.MM.DD"
    work_id     = Column(Integer, ForeignKey("literature_works.id"), nullable=True)
