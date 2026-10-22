from pydantic import BaseModel, Field


class VisitIn(BaseModel):
    sessionId: str = Field(min_length=8, max_length=36)
    path: str = Field(max_length=200)
    referrer: str = Field(default="", max_length=500)
    src: str = Field(default="", max_length=50)


class PeriodStats(BaseModel):
    views: int
    sessions: int
    visitors: int


class VisitTotals(BaseModel):
    today: PeriodStats
    last7: PeriodStats
    last30: PeriodStats
    all: PeriodStats


class SourceCount(BaseModel):
    source: str
    sessions: int


class SessionOut(BaseModel):
    sessionId: str
    startedAt: str      # ISO 8601 UTC
    lastAt: str
    source: str
    device: str
    browser: str
    pages: list[str]
    views: int
    returning: bool


class VisitSummary(BaseModel):
    totals: VisitTotals
    sources: list[SourceCount]
    recent: list[SessionOut]
