from sqlalchemy import Column, Integer, String, Text, Date
from ..database import Base


class SocialActivity(Base):
    __tablename__ = "social_activities"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(200), nullable=False)
    organization = Column(String(200), nullable=False)
    esg_type     = Column(String(20), nullable=True)      # Environmental | Social | Governance；與 sdg_numbers 互斥（擇一分類）
    sdg_numbers  = Column(Text, default="[]")            # JSON array e.g. [1, 3, 13]
    period_from  = Column(Date, nullable=False)
    period_to    = Column(Date, nullable=True)
    reflection   = Column(Text, nullable=False, default="")
    youtube_url  = Column(String(500), nullable=True)
    photos       = Column(Text, default="[]")            # JSON array: [{url, position}]，最多 MAX_SOCIAL_PHOTOS 張
