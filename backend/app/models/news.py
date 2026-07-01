from sqlalchemy import Column, Integer, String, Text, DateTime, func
from ..database import Base


class NewsCache(Base):
    __tablename__ = "news_cache"

    id         = Column(Integer, primary_key=True)
    category   = Column(String(50), nullable=False)   # cate1 / cate2 / ...
    title      = Column(Text, nullable=False)
    url        = Column(Text, nullable=False)
    fetched_at = Column(DateTime, server_default=func.now())
