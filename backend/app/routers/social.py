from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models.social import SocialActivity
from ..schemas.social import SocialActivityOut, SocialActivityIn

router = APIRouter(prefix="/social", tags=["social"])


@router.get("", response_model=list[SocialActivityOut])
def list_social(db: Session = Depends(get_db)):
    rows = db.query(SocialActivity).all()
    return [SocialActivityOut(
        id=r.id, title=r.title, org=r.org, role=r.role,
        period=r.period, category=r.category,
        sdgTag=r.sdg_tag, description=r.description,
    ) for r in rows]


@router.post("", response_model=SocialActivityOut)
def create_social(body: SocialActivityIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = SocialActivity(
        title=body.title, org=body.org, role=body.role, period=body.period,
        category=body.category, sdg_tag=body.sdgTag, description=body.description,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return SocialActivityOut(id=obj.id, title=obj.title, org=obj.org, role=obj.role,
        period=obj.period, category=obj.category, sdgTag=obj.sdg_tag, description=obj.description)


@router.put("/{item_id}", response_model=SocialActivityOut)
def update_social(item_id: int, body: SocialActivityIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(SocialActivity).filter(SocialActivity.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.title = body.title; obj.org = body.org; obj.role = body.role
    obj.period = body.period; obj.category = body.category
    obj.sdg_tag = body.sdgTag; obj.description = body.description
    db.commit(); db.refresh(obj)
    return SocialActivityOut(id=obj.id, title=obj.title, org=obj.org, role=obj.role,
        period=obj.period, category=obj.category, sdgTag=obj.sdg_tag, description=obj.description)


@router.delete("/{item_id}", status_code=204)
def delete_social(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(SocialActivity).filter(SocialActivity.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()
