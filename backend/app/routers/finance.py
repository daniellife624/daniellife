from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models.finance import Holding
from ..schemas.finance import HoldingOut, HoldingIn, PortfolioSummary

router = APIRouter(prefix="/finance", tags=["finance"])


def _to_out(row: Holding) -> HoldingOut:
    return HoldingOut(
        id=row.id, code=row.code, name=row.name, currency=row.currency,
        broker=row.broker, shares=row.shares, avgPrice=row.avg_price,
        currentPrice=row.current_price, dividends=row.dividends,
    )


@router.get("/holdings", response_model=list[HoldingOut])
def list_holdings(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return [_to_out(r) for r in db.query(Holding).all()]


@router.post("/holdings", response_model=HoldingOut)
def create_holding(body: HoldingIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = Holding(
        code=body.code, name=body.name, currency=body.currency, broker=body.broker,
        shares=body.shares, avg_price=body.avgPrice, current_price=body.currentPrice,
        dividends=body.dividends,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _to_out(obj)


@router.put("/holdings/{item_id}", response_model=HoldingOut)
def update_holding(item_id: int, body: HoldingIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(Holding).filter(Holding.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.code = body.code; obj.name = body.name; obj.currency = body.currency
    obj.broker = body.broker; obj.shares = body.shares; obj.avg_price = body.avgPrice
    obj.current_price = body.currentPrice; obj.dividends = body.dividends
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
    return PortfolioSummary(
        totalTWD=round(sum(r.totalValue for r in twd), 2),
        totalUSD=round(sum(r.totalValue for r in usd), 2),
        pnlTWD=round(sum(r.pnl for r in twd), 2),
        pnlUSD=round(sum(r.pnl for r in usd), 2),
        dividendsTWD=round(sum(r.dividends for r in twd), 2),
        dividendsUSD=round(sum(r.dividends for r in usd), 2),
    )
