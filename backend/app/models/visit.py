from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base


class PageView(Base):
    __tablename__ = "page_views"

    id = Column(Integer, primary_key=True, index=True)
    visited_at = Column(DateTime, nullable=False, index=True)          # UTC
    session_id = Column(String(36), nullable=False, index=True)        # 前端每個分頁 session 隨機產生
    visitor_hash = Column(String(16), nullable=False, index=True)      # hash(IP + UA)，不存原始 IP
    path = Column(String(200), nullable=False)
    source = Column(String(50), nullable=False)                        # LinkedIn / 104 / Google / 直接開啟 ...
    referrer = Column(String(500), nullable=False, default="")
    device = Column(String(10), nullable=False)                        # 電腦 / 手機 / 平板
    browser = Column(String(30), nullable=False)
