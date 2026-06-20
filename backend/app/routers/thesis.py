import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models.thesis import ThesisNote, ThesisIdea, ThesisPaper
from ..schemas.thesis import (
    ThesisNoteOut, ThesisNoteIn,
    ThesisIdeaOut, ThesisIdeaIn, ThesisIdeaUpdate,
    ThesisPaperOut, ThesisPaperIn,
)

router = APIRouter(prefix="/thesis", tags=["thesis"])


# ── Note (singleton) ─────────────────────────────────────────────
@router.get("/note", response_model=ThesisNoteOut)
def get_note(db: Session = Depends(get_db), _=Depends(get_current_user)):
    note = db.query(ThesisNote).first()
    if not note:
        note = ThesisNote(content="")
        db.add(note); db.commit(); db.refresh(note)
    return ThesisNoteOut(id=note.id, content=note.content, updatedAt=note.updated_at)


@router.put("/note", response_model=ThesisNoteOut)
def save_note(body: ThesisNoteIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    note = db.query(ThesisNote).first()
    if not note:
        note = ThesisNote(content=body.content)
        db.add(note)
    else:
        note.content = body.content
    db.commit(); db.refresh(note)
    return ThesisNoteOut(id=note.id, content=note.content, updatedAt=note.updated_at)


# ── Ideas (Kanban) ────────────────────────────────────────────────
@router.get("/ideas", response_model=list[ThesisIdeaOut])
def list_ideas(db: Session = Depends(get_db), _=Depends(get_current_user)):
    rows = db.query(ThesisIdea).order_by(ThesisIdea.created_at).all()
    return [ThesisIdeaOut(id=r.id, content=r.content, status=r.status, createdAt=r.created_at) for r in rows]


@router.post("/ideas", response_model=ThesisIdeaOut)
def create_idea(body: ThesisIdeaIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = ThesisIdea(content=body.content, status=body.status)
    db.add(obj); db.commit(); db.refresh(obj)
    return ThesisIdeaOut(id=obj.id, content=obj.content, status=obj.status, createdAt=obj.created_at)


@router.patch("/ideas/{item_id}", response_model=ThesisIdeaOut)
def update_idea_status(item_id: int, body: ThesisIdeaUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisIdea).filter(ThesisIdea.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.status = body.status
    db.commit(); db.refresh(obj)
    return ThesisIdeaOut(id=obj.id, content=obj.content, status=obj.status, createdAt=obj.created_at)


@router.delete("/ideas/{item_id}", status_code=204)
def delete_idea(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisIdea).filter(ThesisIdea.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Papers ────────────────────────────────────────────────────────
@router.get("/papers", response_model=list[ThesisPaperOut])
def list_papers(
    topic: Optional[str] = Query(None),
    journal: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(ThesisPaper)
    if journal:
        q = q.filter(ThesisPaper.journal == journal)
    if keyword:
        q = q.filter(
            ThesisPaper.title.ilike(f"%{keyword}%") |
            ThesisPaper.authors.ilike(f"%{keyword}%") |
            ThesisPaper.purpose.ilike(f"%{keyword}%")
        )
    rows = q.all()
    result = []
    for r in rows:
        topics = json.loads(r.topics) if r.topics else []
        if topic and topic not in topics:
            continue
        result.append(ThesisPaperOut(
            id=r.id, authors=r.authors, year=r.year, title=r.title,
            journal=r.journal, purpose=r.purpose, contribution=r.contribution, topics=topics,
        ))
    return result


@router.post("/papers", response_model=ThesisPaperOut)
def create_paper(body: ThesisPaperIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = ThesisPaper(
        authors=body.authors, year=body.year, title=body.title, journal=body.journal,
        purpose=body.purpose, contribution=body.contribution, topics=json.dumps(body.topics),
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return ThesisPaperOut(id=obj.id, authors=obj.authors, year=obj.year, title=obj.title,
        journal=obj.journal, purpose=obj.purpose, contribution=obj.contribution,
        topics=json.loads(obj.topics))


@router.put("/papers/{item_id}", response_model=ThesisPaperOut)
def update_paper(item_id: int, body: ThesisPaperIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisPaper).filter(ThesisPaper.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.authors = body.authors; obj.year = body.year; obj.title = body.title
    obj.journal = body.journal; obj.purpose = body.purpose; obj.contribution = body.contribution
    obj.topics = json.dumps(body.topics)
    db.commit(); db.refresh(obj)
    return ThesisPaperOut(id=obj.id, authors=obj.authors, year=obj.year, title=obj.title,
        journal=obj.journal, purpose=obj.purpose, contribution=obj.contribution,
        topics=json.loads(obj.topics))


@router.delete("/papers/{item_id}", status_code=204)
def delete_paper(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisPaper).filter(ThesisPaper.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()
