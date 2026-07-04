from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from ..database import Base


class LiteratureWork(Base):
    __tablename__ = "literature_works"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    age_written = Column(Integer, nullable=True)
    period      = Column(Date, nullable=True)       # 頒發日期, stored as date, serialized to "YYYY.MM"
    issuer      = Column(String(200), nullable=True)  # 頒發單位
    category    = Column(String(20), nullable=True)   # 小說 | 散文 | 新詩
    grade_label = Column(String(100), nullable=True)   # 年級標籤，如 "小學 / 五年級"；有填才會自動帶出時間軸事件
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
