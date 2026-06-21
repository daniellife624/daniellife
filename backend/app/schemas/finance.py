from pydantic import BaseModel, computed_field, field_validator


_CURRENCIES = {'TWD', 'USD'}


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

    @field_validator('symbol', 'name', 'broker')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('currency')
    @classmethod
    def currency_choices(cls, v: str) -> str:
        if v not in _CURRENCIES:
            raise ValueError('「幣別」須為 TWD 或 USD')
        return v

    @field_validator('shares', 'avgPrice', 'marketPrice')
    @classmethod
    def positive(cls, v: float, info) -> float:
        if v <= 0:
            raise ValueError(f'「{info.field_name}」須為正數')
        return v


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
