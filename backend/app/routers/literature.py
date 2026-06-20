from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models.literature import TimelineEvent, LiteratureWork
from ..schemas.literature import (
    TimelineEventOut, TimelineEventIn,
    LiteratureWorkOut, LiteratureWorkIn,
)

router = APIRouter(prefix="/literature", tags=["literature"])


# ── Timeline ──────────────────────────────────────────────────────
@router.get("/timeline", response_model=list[TimelineEventOut])
def list_timeline(db: Session = Depends(get_db)):
    return db.query(TimelineEvent).order_by(TimelineEvent.year).all()


@router.post("/timeline", response_model=TimelineEventOut)
def create_timeline(body: TimelineEventIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = TimelineEvent(**body.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj


@router.put("/timeline/{item_id}", response_model=TimelineEventOut)
def update_timeline(item_id: int, body: TimelineEventIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(TimelineEvent).filter(TimelineEvent.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in body.model_dump().items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj


@router.delete("/timeline/{item_id}", status_code=204)
def delete_timeline(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(TimelineEvent).filter(TimelineEvent.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Works ─────────────────────────────────────────────────────────
@router.get("/works", response_model=list[LiteratureWorkOut])
def list_works(db: Session = Depends(get_db)):
    rows = db.query(LiteratureWork).all()
    return [LiteratureWorkOut(
        id=r.id, title=r.title, year=r.year, award=r.award,
        category=r.category, excerpt=r.excerpt, fullText=r.full_text,
    ) for r in rows]


@router.post("/works", response_model=LiteratureWorkOut)
def create_work(body: LiteratureWorkIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = LiteratureWork(
        title=body.title, year=body.year, award=body.award,
        category=body.category, excerpt=body.excerpt, full_text=body.fullText,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return LiteratureWorkOut(id=obj.id, title=obj.title, year=obj.year, award=obj.award,
        category=obj.category, excerpt=obj.excerpt, fullText=obj.full_text)


@router.put("/works/{item_id}", response_model=LiteratureWorkOut)
def update_work(item_id: int, body: LiteratureWorkIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(LiteratureWork).filter(LiteratureWork.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.title = body.title; obj.year = body.year; obj.award = body.award
    obj.category = body.category; obj.excerpt = body.excerpt; obj.full_text = body.fullText
    db.commit(); db.refresh(obj)
    return LiteratureWorkOut(id=obj.id, title=obj.title, year=obj.year, award=obj.award,
        category=obj.category, excerpt=obj.excerpt, fullText=obj.full_text)


@router.delete("/works/{item_id}", status_code=204)
def delete_work(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(LiteratureWork).filter(LiteratureWork.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()
