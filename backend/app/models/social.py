from sqlalchemy import Column, Integer, String, Text
from ..database import Base


class SocialActivity(Base):
    __tablename__ = "social_activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    org = Column(String(200), nullable=False)
    role = Column(String(200), nullable=False)
    period = Column(String(100), nullable=False)
    category = Column(String(5), nullable=False)    # E | S | G
    sdg_tag = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
