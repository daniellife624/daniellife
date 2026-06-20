from pydantic import BaseModel, computed_field


class HoldingOut(BaseModel):
    id: int
    code: str
    name: str
    currency: str
    broker: str
    shares: float
    avgPrice: float
    currentPrice: float
    dividends: float

    model_config = {"from_attributes": True, "populate_by_name": True}

    @computed_field
    @property
    def totalValue(self) -> float:
        return round(self.shares * self.currentPrice, 2)

    @computed_field
    @property
    def pnl(self) -> float:
        return round((self.currentPrice - self.avgPrice) * self.shares, 2)

    @computed_field
    @property
    def returnRate(self) -> float:
        if self.avgPrice == 0:
            return 0.0
        return round((self.currentPrice - self.avgPrice) / self.avgPrice * 100, 2)

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "avg_price"):
            data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
            data["avgPrice"] = data.pop("avg_price")
            data["currentPrice"] = data.pop("current_price")
            return cls(**data)
        return super().model_validate(obj, **kwargs)


class HoldingIn(BaseModel):
    code: str
    name: str
    currency: str
    broker: str
    shares: float
    avgPrice: float
    currentPrice: float
    dividends: float = 0.0


class PortfolioSummary(BaseModel):
    totalTWD: float
    totalUSD: float
    pnlTWD: float
    pnlUSD: float
    dividendsTWD: float
    dividendsUSD: float
