from sqlalchemy import Column, Integer, String, Text, Date
from ..database import Base


class SocialActivity(Base):
    __tablename__ = "social_activities"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(200), nullable=False)
    organization = Column(String(200), nullable=False)
    esg_type     = Column(String(20), nullable=False)    # Environmental | Social | Governance
    sdg_numbers  = Column(Text, default="[]")            # JSON array e.g. [1, 3, 13]
    period_from  = Column(Date, nullable=False)
    period_to    = Column(Date, nullable=True)
    contribution = Column(Text, nullable=False)
    reflection   = Column(Text, nullable=False, default="")
    photo_url    = Column(String(500), nullable=True)
    photo_position = Column(String(20), nullable=False, default="50% 50%")
