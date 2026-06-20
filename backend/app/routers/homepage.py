import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models import homepage as m
from ..schemas import homepage as s

router = APIRouter(prefix="/homepage", tags=["homepage"])


# ── Internships ──────────────────────────────────────────────────
@router.get("/internships", response_model=list[s.InternshipOut])
def list_internships(db: Session = Depends(get_db)):
    return db.query(m.Internship).all()


@router.post("/internships", response_model=s.InternshipOut)
def create_internship(body: s.InternshipIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.Internship(**body.model_dump() | {"photos": json.dumps(body.photos)})
    db.add(obj); db.commit(); db.refresh(obj)
    return obj


@router.put("/internships/{item_id}", response_model=s.InternshipOut)
def update_internship(item_id: int, body: s.InternshipIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Internship).filter(m.Internship.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in body.model_dump().items():
        setattr(obj, k, json.dumps(v) if k == "photos" else v)
    db.commit(); db.refresh(obj)
    return obj


@router.delete("/internships/{item_id}", status_code=204)
def delete_internship(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Internship).filter(m.Internship.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Projects ─────────────────────────────────────────────────────
@router.get("/projects", response_model=list[s.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(m.Project).all()


@router.post("/projects", response_model=s.ProjectOut)
def create_project(body: s.ProjectIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.Project(**body.model_dump() | {"tech": json.dumps(body.tech), "links": json.dumps(body.links)})
    db.add(obj); db.commit(); db.refresh(obj)
    return obj


@router.put("/projects/{item_id}", response_model=s.ProjectOut)
def update_project(item_id: int, body: s.ProjectIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Project).filter(m.Project.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in body.model_dump().items():
        setattr(obj, k, json.dumps(v) if k in ("tech", "links") else v)
    db.commit(); db.refresh(obj)
    return obj


@router.delete("/projects/{item_id}", status_code=204)
def delete_project(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Project).filter(m.Project.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Certs / Academic / FuturePlan (read-only public) ─────────────
@router.get("/certs", response_model=list[s.CertItemOut])
def list_certs(db: Session = Depends(get_db)):
    return db.query(m.CertItem).all()


@router.get("/academic", response_model=list[s.AcademicMilestoneOut])
def list_academic(db: Session = Depends(get_db)):
    return db.query(m.AcademicMilestone).order_by(m.AcademicMilestone.x).all()


@router.get("/future-plans", response_model=list[s.FuturePlanOut])
def list_future_plans(db: Session = Depends(get_db)):
    return db.query(m.FuturePlan).order_by(m.FuturePlan.order).all()
