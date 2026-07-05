import json
import uuid
from datetime import date
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models.social import SocialActivity
from ..schemas.social import SocialActivityOut, SocialActivityIn, PhotoPositionIn

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads" / "social"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE_MB = 10

router = APIRouter(prefix="/social", tags=["social"])


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


def _to_out(r) -> SocialActivityOut:
    return SocialActivityOut(
        id=r.id,
        name=r.name,
        organization=r.organization,
        esgType=r.esg_type,
        sdgNumbers=json.loads(r.sdg_numbers) if r.sdg_numbers else [],
        periodFrom=r.period_from.isoformat() if r.period_from else "",
        periodTo=r.period_to.isoformat() if r.period_to else None,
        contribution=r.contribution,
        reflection=r.reflection or "",
        photoUrl=r.photo_url,
        photoPosition=r.photo_position or "50% 50%",
    )


@router.get("", response_model=list[SocialActivityOut])
def list_social(db: Session = Depends(get_db)):
    return [_to_out(r) for r in db.query(SocialActivity).all()]


@router.post("", response_model=SocialActivityOut)
def create_social(body: SocialActivityIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = SocialActivity(
        name=body.name, organization=body.organization,
        esg_type=body.esgType, sdg_numbers=json.dumps(body.sdgNumbers),
        period_from=_parse_date(body.periodFrom),
        period_to=_parse_date(body.periodTo) if body.periodTo else None,
        contribution=body.contribution, reflection=body.reflection,
        photo_url=body.photoUrl,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _to_out(obj)


@router.put("/{item_id}", response_model=SocialActivityOut)
def update_social(item_id: int, body: SocialActivityIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(SocialActivity).filter(SocialActivity.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.name = body.name; obj.organization = body.organization
    obj.esg_type = body.esgType; obj.sdg_numbers = json.dumps(body.sdgNumbers)
    obj.period_from = _parse_date(body.periodFrom)
    obj.period_to = _parse_date(body.periodTo) if body.periodTo else None
    obj.contribution = body.contribution; obj.reflection = body.reflection
    db.commit(); db.refresh(obj)
    return _to_out(obj)


@router.delete("/{item_id}", status_code=204)
def delete_social(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(SocialActivity).filter(SocialActivity.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


@router.post("/{item_id}/photo", response_model=SocialActivityOut)
async def upload_social_photo(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    obj = db.query(SocialActivity).filter(SocialActivity.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"不支援的檔案類型：{file.content_type}")
    content = await file.read()
    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, f"檔案大小超過 {MAX_SIZE_MB}MB 限制")
    ext = Path(file.filename or "photo.jpg").suffix.lower() or ".jpg"
    filename = f"{item_id}_{uuid.uuid4().hex[:8]}{ext}"
    (UPLOAD_DIR / filename).write_bytes(content)
    if obj.photo_url:
        old = UPLOAD_DIR / Path(obj.photo_url).name
        if old.exists():
            old.unlink()
    obj.photo_url = f"/uploads/social/{filename}"
    db.commit(); db.refresh(obj)
    return _to_out(obj)


@router.delete("/{item_id}/photo", response_model=SocialActivityOut)
def delete_social_photo(
    item_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    obj = db.query(SocialActivity).filter(SocialActivity.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    if obj.photo_url:
        target = UPLOAD_DIR / Path(obj.photo_url).name
        if target.exists():
            target.unlink()
    obj.photo_url = None
    db.commit(); db.refresh(obj)
    return _to_out(obj)


@router.patch("/{item_id}/photo-position", response_model=SocialActivityOut)
def update_social_photo_position(
    item_id: int,
    body: PhotoPositionIn,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    obj = db.query(SocialActivity).filter(SocialActivity.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.photo_position = body.position
    db.commit(); db.refresh(obj)
    return _to_out(obj)
