import json
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models import activities as m
from ..schemas import activities as s

router = APIRouter(prefix="/activities", tags=["activities"])


def _parse_date(st: str | None) -> date | None:
    if not st:
        return None
    st = st.replace(".", "-").replace("/", "-")
    parts = st.split("-")
    try:
        if len(parts) == 2:
            return date(int(parts[0]), int(parts[1]), 1)
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return None


def _parse_period(period: str):
    """'2021/04 – 2023/06' → (date, date|None)"""
    sep = "–" if "–" in period else "-"
    parts = [p.strip() for p in period.split(sep, 1)]
    start = _parse_date(parts[0])
    end = None
    if len(parts) > 1 and parts[1] not in ("至今", "present", "now", ""):
        end = _parse_date(parts[1])
    return start, end


def _fmt_period(start: date | None, end: date | None) -> str:
    if start is None:
        return ""
    s = start.strftime("%Y/%m")
    return f"{s} – {end.strftime('%Y/%m')}" if end else f"{s} – 至今"


def _exp_to_out(r) -> s.ExperienceOut:
    return s.ExperienceOut(
        id=r.id, type=r.type, title=r.title, organization=r.organization,
        period=_fmt_period(r.start_date, r.end_date),
        startDate=r.start_date.isoformat() if r.start_date else None,
        endDate=r.end_date.isoformat() if r.end_date else None,
        contribution=r.contribution,
        photos=json.loads(r.photos) if r.photos else [],
    )


def _travel_to_out(r) -> s.TravelEntryOut:
    return s.TravelEntryOut(
        id=r.id, country=r.country, city=r.city, continent=r.continent,
        visitedAt=r.visited_at.isoformat() if r.visited_at else "",
        journal=r.journal, companions=r.companions,
        activities=r.activities, purchases=r.purchases,
        photos=json.loads(r.photos) if r.photos else [],
    )


# ── Experiences ───────────────────────────────────────────────────
@router.get("/experiences", response_model=list[s.ExperienceOut])
def list_experiences(db: Session = Depends(get_db)):
    return [_exp_to_out(r) for r in db.query(m.Experience).all()]


@router.post("/experiences", response_model=s.ExperienceOut)
def create_experience(body: s.ExperienceIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    start, end = _parse_period(body.period)
    obj = m.Experience(
        type=body.type, title=body.title, organization=body.organization,
        start_date=start, end_date=end,
        contribution=body.contribution, photos=json.dumps(body.photos),
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _exp_to_out(obj)


@router.put("/experiences/{item_id}", response_model=s.ExperienceOut)
def update_experience(item_id: int, body: s.ExperienceIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Experience).filter(m.Experience.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    start, end = _parse_period(body.period)
    obj.type = body.type; obj.title = body.title; obj.organization = body.organization
    obj.start_date = start; obj.end_date = end
    obj.contribution = body.contribution; obj.photos = json.dumps(body.photos)
    db.commit(); db.refresh(obj)
    return _exp_to_out(obj)


@router.delete("/experiences/{item_id}", status_code=204)
def delete_experience(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Experience).filter(m.Experience.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Travel Entries ────────────────────────────────────────────────
@router.get("/travel", response_model=list[s.TravelEntryOut])
def list_travel(db: Session = Depends(get_db)):
    return [_travel_to_out(r) for r in db.query(m.TravelEntry).all()]


@router.post("/travel", response_model=s.TravelEntryOut)
def create_travel(body: s.TravelEntryIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.TravelEntry(
        country=body.country, city=body.city, continent=body.continent,
        visited_at=_parse_date(body.visitedAt),
        journal=body.journal, companions=body.companions,
        activities=body.activities, purchases=body.purchases,
        photos=json.dumps(body.photos),
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _travel_to_out(obj)


@router.put("/travel/{item_id}", response_model=s.TravelEntryOut)
def update_travel(item_id: int, body: s.TravelEntryIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.TravelEntry).filter(m.TravelEntry.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.country = body.country; obj.city = body.city; obj.continent = body.continent
    obj.visited_at = _parse_date(body.visitedAt)
    obj.journal = body.journal; obj.companions = body.companions
    obj.activities = body.activities; obj.purchases = body.purchases
    obj.photos = json.dumps(body.photos)
    db.commit(); db.refresh(obj)
    return _travel_to_out(obj)


@router.delete("/travel/{item_id}", status_code=204)
def delete_travel(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.TravelEntry).filter(m.TravelEntry.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()
