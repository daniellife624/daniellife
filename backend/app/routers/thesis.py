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
from ..notion_sync import sync_paper_notes, NotionSyncError

router = APIRouter(prefix="/thesis", tags=["thesis"])


def _paper_out(r: ThesisPaper) -> ThesisPaperOut:
    return ThesisPaperOut(
        id=r.id, topic=r.topic, name=r.name, journal=r.journal, authors=r.authors,
        year=r.year, purpose=r.purpose, contribution=r.contribution,
        notes=r.notes, notionUrl=r.notion_url,
    )


# ── Note (singleton) ─────────────────────────────────────────────
@router.get("/note", response_model=ThesisNoteOut)
def get_note(db: Session = Depends(get_db), _=Depends(get_current_user)):
    note = db.query(ThesisNote).first()
    if not note:
        note = ThesisNote(content="")
        db.add(note); db.commit(); db.refresh(note)
    return ThesisNoteOut.from_orm_row(note)


@router.put("/note", response_model=ThesisNoteOut)
def save_note(body: ThesisNoteIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    note = db.query(ThesisNote).first()
    if not note:
        note = ThesisNote(content=body.content)
        db.add(note)
    else:
        note.content = body.content
    db.commit(); db.refresh(note)
    return ThesisNoteOut.from_orm_row(note)


# ── Ideas (Kanban) ────────────────────────────────────────────────
@router.get("/ideas", response_model=list[ThesisIdeaOut])
def list_ideas(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return [ThesisIdeaOut.from_orm_row(r) for r in db.query(ThesisIdea).order_by(ThesisIdea.created_at).all()]


@router.post("/ideas", response_model=ThesisIdeaOut)
def create_idea(body: ThesisIdeaIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = ThesisIdea(title=body.title, content=body.content, status=body.status)
    db.add(obj); db.commit(); db.refresh(obj)
    return ThesisIdeaOut.from_orm_row(obj)


@router.patch("/ideas/{item_id}", response_model=ThesisIdeaOut)
def update_idea(item_id: int, body: ThesisIdeaUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisIdea).filter(ThesisIdea.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    if body.title is not None:
        obj.title = body.title
    if body.content is not None:
        obj.content = body.content
    if body.status is not None:
        obj.status = body.status
    db.commit(); db.refresh(obj)
    return ThesisIdeaOut.from_orm_row(obj)


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
    if topic:
        q = q.filter(ThesisPaper.topic == topic)
    if journal:
        q = q.filter(ThesisPaper.journal == journal)
    if keyword:
        q = q.filter(
            ThesisPaper.name.ilike(f"%{keyword}%") |
            ThesisPaper.authors.ilike(f"%{keyword}%") |
            ThesisPaper.purpose.ilike(f"%{keyword}%")
        )
    return [_paper_out(r) for r in q.all()]


@router.post("/papers", response_model=ThesisPaperOut)
def create_paper(body: ThesisPaperIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = ThesisPaper(
        topic=body.topic, name=body.name, journal=body.journal, authors=body.authors,
        year=body.year, purpose=body.purpose, contribution=body.contribution,
        notion_url=body.notionUrl,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _paper_out(obj)


@router.put("/papers/{item_id}", response_model=ThesisPaperOut)
def update_paper(item_id: int, body: ThesisPaperIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisPaper).filter(ThesisPaper.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.topic = body.topic; obj.name = body.name; obj.journal = body.journal
    obj.authors = body.authors; obj.year = body.year; obj.purpose = body.purpose
    obj.contribution = body.contribution; obj.notion_url = body.notionUrl
    db.commit(); db.refresh(obj)
    return _paper_out(obj)


@router.delete("/papers/{item_id}", status_code=204)
def delete_paper(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisPaper).filter(ThesisPaper.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Notion sync (paper notes) ───────────────────────────────────────
@router.post("/papers/sync-notion")
def sync_notion(db: Session = Depends(get_db), _=Depends(get_current_user)):
    papers = db.query(ThesisPaper).filter(ThesisPaper.notion_url.isnot(None), ThesisPaper.notion_url != "").all()
    synced: list[int] = []
    failed: list[dict] = []
    for p in papers:
        try:
            p.notes = sync_paper_notes(p.notion_url, p.id)
            synced.append(p.id)
        except NotionSyncError as e:
            failed.append({"id": p.id, "name": p.name, "error": str(e)})
        except Exception as e:
            failed.append({"id": p.id, "name": p.name, "error": f"未預期的錯誤：{e}"})
    db.commit()
    return {"synced": synced, "failed": failed}
