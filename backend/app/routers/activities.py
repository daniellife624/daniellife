import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models import activities as m
from ..schemas import activities as s

router = APIRouter(prefix="/activities", tags=["activities"])


# ── Experiences ───────────────────────────────────────────────────
@router.get("/experiences", response_model=list[s.ExperienceOut])
def list_experiences(db: Session = Depends(get_db)):
    return db.query(m.Experience).all()


@router.post("/experiences", response_model=s.ExperienceOut)
def create_experience(body: s.ExperienceIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.Experience(**body.model_dump() | {"photos": json.dumps(body.photos)})
    db.add(obj); db.commit(); db.refresh(obj)
    return obj


@router.put("/experiences/{item_id}", response_model=s.ExperienceOut)
def update_experience(item_id: int, body: s.ExperienceIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Experience).filter(m.Experience.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in body.model_dump().items():
        setattr(obj, k, json.dumps(v) if k == "photos" else v)
    db.commit(); db.refresh(obj)
    return obj


@router.delete("/experiences/{item_id}", status_code=204)
def delete_experience(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Experience).filter(m.Experience.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Travel Entries ────────────────────────────────────────────────
@router.get("/travel", response_model=list[s.TravelEntryOut])
def list_travel(db: Session = Depends(get_db)):
    rows = db.query(m.TravelEntry).all()
    result = []
    for row in rows:
        result.append(s.TravelEntryOut(
            id=row.id, country=row.country, city=row.city,
            continent=row.continent, visitedAt=row.visited_at,
            journal=row.journal, companions=row.companions,
            activities=row.activities, purchases=row.purchases,
            photos=json.loads(row.photos) if row.photos else [],
        ))
    return result


@router.post("/travel", response_model=s.TravelEntryOut)
def create_travel(body: s.TravelEntryIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.TravelEntry(
        country=body.country, city=body.city, continent=body.continent,
        visited_at=body.visitedAt, journal=body.journal, companions=body.companions,
        activities=body.activities, purchases=body.purchases,
        photos=json.dumps(body.photos),
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return s.TravelEntryOut(
        id=obj.id, country=obj.country, city=obj.city,
        continent=obj.continent, visitedAt=obj.visited_at,
        journal=obj.journal, companions=obj.companions,
        activities=obj.activities, purchases=obj.purchases,
        photos=json.loads(obj.photos),
    )


@router.put("/travel/{item_id}", response_model=s.TravelEntryOut)
def update_travel(item_id: int, body: s.TravelEntryIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.TravelEntry).filter(m.TravelEntry.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.country = body.country; obj.city = body.city; obj.continent = body.continent
    obj.visited_at = body.visitedAt; obj.journal = body.journal
    obj.companions = body.companions; obj.activities = body.activities
    obj.purchases = body.purchases; obj.photos = json.dumps(body.photos)
    db.commit(); db.refresh(obj)
    return s.TravelEntryOut(
        id=obj.id, country=obj.country, city=obj.city,
        continent=obj.continent, visitedAt=obj.visited_at,
        journal=obj.journal, companions=obj.companions,
        activities=obj.activities, purchases=obj.purchases,
        photos=json.loads(obj.photos),
    )


@router.delete("/travel/{item_id}", status_code=204)
def delete_travel(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.TravelEntry).filter(m.TravelEntry.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()
