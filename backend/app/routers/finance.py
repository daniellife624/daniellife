from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models.finance import Holding
from ..schemas.finance import HoldingOut, HoldingIn, PortfolioSummary

router = APIRouter(prefix="/finance", tags=["finance"])


def _to_out(row: Holding) -> HoldingOut:
    return HoldingOut(
        id=row.id, symbol=row.symbol, name=row.name, currency=row.currency,
        broker=row.broker, shares=row.shares, avgPrice=row.avg_price,
        marketPrice=row.market_price, dividend=row.dividend,
    )


@router.get("/holdings", response_model=list[HoldingOut])
def list_holdings(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return [_to_out(r) for r in db.query(Holding).all()]


@router.post("/holdings", response_model=HoldingOut)
def create_holding(body: HoldingIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = Holding(
        symbol=body.symbol, name=body.name, currency=body.currency, broker=body.broker,
        shares=body.shares, avg_price=body.avgPrice, market_price=body.marketPrice,
        dividend=body.dividend,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _to_out(obj)


@router.put("/holdings/{item_id}", response_model=HoldingOut)
def update_holding(item_id: int, body: HoldingIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(Holding).filter(Holding.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.symbol = body.symbol; obj.name = body.name; obj.currency = body.currency
    obj.broker = body.broker; obj.shares = body.shares; obj.avg_price = body.avgPrice
    obj.market_price = body.marketPrice; obj.dividend = body.dividend
    db.commit(); db.refresh(obj)
    return _to_out(obj)


@router.delete("/holdings/{item_id}", status_code=204)
def delete_holding(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(Holding).filter(Holding.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


@router.get("/portfolio-summary", response_model=PortfolioSummary)
def portfolio_summary(db: Session = Depends(get_db), _=Depends(get_current_user)):
    rows = [_to_out(r) for r in db.query(Holding).all()]
    twd = [r for r in rows if r.currency == "TWD"]
    usd = [r for r in rows if r.currency == "USD"]

    def safe_rate(pnl, cost):
        return round(pnl / cost * 100, 2) if cost else 0.0

    twd_value = round(sum(r.currentValue for r in twd), 2)
    twd_cost  = round(sum(r.shares * r.avgPrice for r in twd), 2)
    twd_pnl   = round(sum(r.pnl for r in twd), 2)
    usd_value = round(sum(r.currentValue for r in usd), 2)
    usd_cost  = round(sum(r.shares * r.avgPrice for r in usd), 2)
    usd_pnl   = round(sum(r.pnl for r in usd), 2)

    return PortfolioSummary(
        twdValue=twd_value, twdCost=twd_cost, twdPnl=twd_pnl,
        twdReturnRate=safe_rate(twd_pnl, twd_cost),
        twdDividend=round(sum(r.dividend for r in twd), 2),
        usdValue=usd_value, usdCost=usd_cost, usdPnl=usd_pnl,
        usdReturnRate=safe_rate(usd_pnl, usd_cost),
        updatedAt=date.today().strftime("%Y/%m/%d"),
    )
