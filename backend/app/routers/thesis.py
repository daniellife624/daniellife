import uuid
from pathlib import Path as FsPath
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models.thesis import ThesisNote, ThesisIdea, ThesisPaper
from ..schemas.thesis import (
    ThesisNoteOut, ThesisNoteIn,
    ThesisIdeaOut, ThesisIdeaIn, ThesisIdeaUpdate,
    ThesisPaperOut, ThesisPaperIn, ThesisPaperNotesIn,
)

router = APIRouter(prefix="/thesis", tags=["thesis"])

NOTE_IMG_DIR = FsPath(__file__).resolve().parent.parent.parent / "uploads" / "thesis_notes"
NOTE_IMG_DIR.mkdir(parents=True, exist_ok=True)
NOTE_IMG_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
NOTE_IMG_MAX_SIZE_MB = 10


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
    return q.all()


@router.post("/papers", response_model=ThesisPaperOut)
def create_paper(body: ThesisPaperIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = ThesisPaper(
        topic=body.topic, name=body.name, journal=body.journal, authors=body.authors,
        year=body.year, purpose=body.purpose, contribution=body.contribution,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj


@router.put("/papers/{item_id}", response_model=ThesisPaperOut)
def update_paper(item_id: int, body: ThesisPaperIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisPaper).filter(ThesisPaper.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.topic = body.topic; obj.name = body.name; obj.journal = body.journal
    obj.authors = body.authors; obj.year = body.year; obj.purpose = body.purpose
    obj.contribution = body.contribution
    db.commit(); db.refresh(obj)
    return obj


@router.delete("/papers/{item_id}", status_code=204)
def delete_paper(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisPaper).filter(ThesisPaper.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Paper notes (per-row rich note + pasted images) ────────────────
@router.patch("/papers/{item_id}/notes", response_model=ThesisPaperOut)
def update_paper_notes(item_id: int, body: ThesisPaperNotesIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(ThesisPaper).filter(ThesisPaper.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.notes = body.notes
    db.commit(); db.refresh(obj)
    return obj


@router.post("/papers/{item_id}/notes/image")
async def upload_paper_note_image(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    obj = db.query(ThesisPaper).filter(ThesisPaper.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    if file.content_type not in NOTE_IMG_ALLOWED_TYPES:
        raise HTTPException(400, f"不支援的檔案類型：{file.content_type}")
    content = await file.read()
    if len(content) > NOTE_IMG_MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, f"檔案大小超過 {NOTE_IMG_MAX_SIZE_MB}MB 限制")
    ext = FsPath(file.filename or "image.png").suffix.lower() or ".png"
    filename = f"{item_id}_{uuid.uuid4().hex[:8]}{ext}"
    (NOTE_IMG_DIR / filename).write_bytes(content)
    return {"url": f"/uploads/thesis_notes/{filename}"}
