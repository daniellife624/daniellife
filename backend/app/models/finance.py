from sqlalchemy import Column, Integer, String, Float
from ..database import Base


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), nullable=False)
    name = Column(String(200), nullable=False)
    currency = Column(String(5), nullable=False)   # TWD | USD
    broker = Column(String(100), nullable=False)
    shares = Column(Float, nullable=False)
    avg_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    dividends = Column(Float, default=0.0)
