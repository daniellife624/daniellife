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
MAX_SOCIAL_PHOTOS = 2

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


def _normalize_photos(raw: str | None) -> list[dict]:
    """相容舊格式（純字串陣列）與新格式（{url, position} 物件陣列）。"""
    if not raw:
        return []
    items = json.loads(raw)
    normalized = []
    for item in items:
        if isinstance(item, str):
            normalized.append({"url": item, "position": "50% 50%"})
        else:
            normalized.append({"url": item.get("url"), "position": item.get("position") or "50% 50%"})
    return normalized


def _to_out(r) -> SocialActivityOut:
    return SocialActivityOut(
        id=r.id,
        name=r.name,
        organization=r.organization,
        esgType=r.esg_type,
        sdgNumbers=json.loads(r.sdg_numbers) if r.sdg_numbers else [],
        periodFrom=r.period_from.isoformat() if r.period_from else "",
        periodTo=r.period_to.isoformat() if r.period_to else None,
        reflection=r.reflection or "",
        youtubeUrl=r.youtube_url,
        photos=_normalize_photos(r.photos),
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
        reflection=body.reflection, youtube_url=body.youtubeUrl,
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
    obj.reflection = body.reflection; obj.youtube_url = body.youtubeUrl
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
    photos = _normalize_photos(obj.photos)
    if len(photos) >= MAX_SOCIAL_PHOTOS:
        raise HTTPException(400, f"社會參與照片最多上傳 {MAX_SOCIAL_PHOTOS} 張")
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"不支援的檔案類型：{file.content_type}")
    content = await file.read()
    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, f"檔案大小超過 {MAX_SIZE_MB}MB 限制")
    ext = Path(file.filename or "photo.jpg").suffix.lower() or ".jpg"
    filename = f"{item_id}_{uuid.uuid4().hex[:8]}{ext}"
    (UPLOAD_DIR / filename).write_bytes(content)
    photos.append({"url": f"/uploads/social/{filename}", "position": "50% 50%"})
    obj.photos = json.dumps(photos)
    db.commit(); db.refresh(obj)
    return _to_out(obj)


@router.delete("/{item_id}/photo", response_model=SocialActivityOut)
def delete_social_photo(
    item_id: int,
    url: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    obj = db.query(SocialActivity).filter(SocialActivity.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    photos = _normalize_photos(obj.photos)
    photos = [p for p in photos if p["url"] != url]
    obj.photos = json.dumps(photos)
    db.commit(); db.refresh(obj)
    target = UPLOAD_DIR / Path(url).name
    if target.exists():
        target.unlink()
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
    photos = _normalize_photos(obj.photos)
    found = False
    for p in photos:
        if p["url"] == body.url:
            p["position"] = body.position
            found = True
    if not found:
        raise HTTPException(404, "Photo not found")
    obj.photos = json.dumps(photos)
    db.commit(); db.refresh(obj)
    return _to_out(obj)
