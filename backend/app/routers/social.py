import json
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models.social import SocialActivity
from ..schemas.social import SocialActivityOut, SocialActivityIn

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
    obj.photo_url = body.photoUrl
    db.commit(); db.refresh(obj)
    return _to_out(obj)


@router.delete("/{item_id}", status_code=204)
def delete_social(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(SocialActivity).filter(SocialActivity.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()
