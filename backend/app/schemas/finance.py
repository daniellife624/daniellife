from pydantic import BaseModel, computed_field
from datetime import date


class HoldingOut(BaseModel):
    id: int
    symbol: str
    name: str
    currency: str
    broker: str
    shares: float
    avgPrice: float
    marketPrice: float
    dividend: float

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def currentValue(self) -> float:
        return round(self.shares * self.marketPrice, 2)

    @computed_field
    @property
    def pnl(self) -> float:
        return round((self.marketPrice - self.avgPrice) * self.shares, 2)

    @computed_field
    @property
    def returnRate(self) -> float:
        if self.avgPrice == 0:
            return 0.0
        return round((self.marketPrice - self.avgPrice) / self.avgPrice * 100, 2)


class HoldingIn(BaseModel):
    symbol: str
    name: str
    currency: str
    broker: str
    shares: float
    avgPrice: float
    marketPrice: float
    dividend: float = 0.0


class PortfolioSummary(BaseModel):
    twdValue: float
    twdCost: float
    twdPnl: float
    twdReturnRate: float
    twdDividend: float
    usdValue: float
    usdCost: float
    usdPnl: float
    usdReturnRate: float
    updatedAt: str
