from sqlalchemy import Column, Integer, String, Text
from ..database import Base


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)      # leadership | club
    title = Column(String(200), nullable=False)
    organization = Column(String(200), nullable=False)
    period = Column(String(100), nullable=False)
    contribution = Column(Text, nullable=False)
    photos = Column(Text, default="[]")            # JSON array of URLs


class TravelEntry(Base):
    __tablename__ = "travel_entries"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    continent = Column(String(50), nullable=False)
    visited_at = Column(String(50), nullable=False)
    journal = Column(Text, nullable=True)
    companions = Column(Text, nullable=True)
    activities = Column(Text, nullable=True)
    purchases = Column(Text, nullable=True)
    photos = Column(Text, default="[]")            # JSON array of URLs
