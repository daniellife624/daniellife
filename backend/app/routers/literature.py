from datetime import date
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


def _parse_date(s: str | None) -> date | None:
    if not s:
        return None
    s = s.replace(".", "-").replace("/", "-")
    parts = s.split("-")
    try:
        if len(parts) == 2:
            return date(int(parts[0]), int(parts[1]), 1)
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return None


def _work_to_out(r) -> LiteratureWorkOut:
    return LiteratureWorkOut(
        id=r.id, title=r.title, ageWritten=r.age_written,
        period=r.period.strftime("%Y.%m") if r.period else None,
        awards=r.awards or "", summary=r.summary, fullText=r.full_text,
    )


def _event_to_out(r) -> TimelineEventOut:
    return TimelineEventOut(
        id=r.id, gradeLabel=r.grade_label, awardTitle=r.award_title,
        result=r.result,
        date=r.date.strftime("%Y.%m.%d") if r.date else "",
        workId=r.work_id,
    )


# ── Works ─────────────────────────────────────────────────────────
@router.get("/works", response_model=list[LiteratureWorkOut])
def list_works(db: Session = Depends(get_db)):
    return [_work_to_out(r) for r in db.query(LiteratureWork).all()]


@router.post("/works", response_model=LiteratureWorkOut)
def create_work(body: LiteratureWorkIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = LiteratureWork(
        title=body.title, age_written=body.ageWritten,
        period=_parse_date(body.period) if body.period else None,
        awards=body.awards, summary=body.summary, full_text=body.fullText,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _work_to_out(obj)


@router.put("/works/{item_id}", response_model=LiteratureWorkOut)
def update_work(item_id: int, body: LiteratureWorkIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(LiteratureWork).filter(LiteratureWork.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.title = body.title; obj.age_written = body.ageWritten
    obj.period = _parse_date(body.period) if body.period else None
    obj.awards = body.awards; obj.summary = body.summary; obj.full_text = body.fullText
    db.commit(); db.refresh(obj)
    return _work_to_out(obj)


@router.delete("/works/{item_id}", status_code=204)
def delete_work(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(LiteratureWork).filter(LiteratureWork.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Timeline ──────────────────────────────────────────────────────
@router.get("/timeline", response_model=list[TimelineEventOut])
def list_timeline(db: Session = Depends(get_db)):
    return [_event_to_out(r) for r in db.query(TimelineEvent).order_by(TimelineEvent.date).all()]


@router.post("/timeline", response_model=TimelineEventOut)
def create_timeline(body: TimelineEventIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = TimelineEvent(
        grade_label=body.gradeLabel, award_title=body.awardTitle,
        result=body.result, date=_parse_date(body.date), work_id=body.workId,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _event_to_out(obj)


@router.put("/timeline/{item_id}", response_model=TimelineEventOut)
def update_timeline(item_id: int, body: TimelineEventIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(TimelineEvent).filter(TimelineEvent.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.grade_label = body.gradeLabel; obj.award_title = body.awardTitle
    obj.result = body.result; obj.date = _parse_date(body.date); obj.work_id = body.workId
    db.commit(); db.refresh(obj)
    return _event_to_out(obj)


@router.delete("/timeline/{item_id}", status_code=204)
def delete_timeline(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(TimelineEvent).filter(TimelineEvent.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()
