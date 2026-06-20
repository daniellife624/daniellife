import json
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models import homepage as m
from ..schemas import homepage as s

router = APIRouter(prefix="/homepage", tags=["homepage"])


def _parse_date(st: str | None) -> date | None:
    if not st:
        return None
    st = st.replace(".", "-").replace("/", "-")
    parts = st.split("-")
    try:
        if len(parts) == 2:
            return date(int(parts[0]), int(parts[1]), 1)
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return None


def _fmt_period(start: date | None, end: date | None) -> str:
    if start is None:
        return ""
    s = start.strftime("%Y/%m")
    return f"{s} – {end.strftime('%Y/%m')}" if end else f"{s} – 至今"


def _intern_to_out(r) -> s.InternshipOut:
    return s.InternshipOut(
        id=r.id, company=r.company, department=r.department,
        startDate=r.start_date.isoformat() if r.start_date else None,
        endDate=r.end_date.isoformat() if r.end_date else None,
        period=_fmt_period(r.start_date, r.end_date),
        contribution=r.contribution,
        photos=json.loads(r.photos) if r.photos else [],
    )


# ── Internships ──────────────────────────────────────────────────
@router.get("/internships", response_model=list[s.InternshipOut])
def list_internships(db: Session = Depends(get_db)):
    return [_intern_to_out(r) for r in db.query(m.Internship).all()]


@router.post("/internships", response_model=s.InternshipOut)
def create_internship(body: s.InternshipIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.Internship(
        company=body.company, department=body.department,
        start_date=_parse_date(body.startDate),
        end_date=_parse_date(body.endDate),
        contribution=body.contribution, photos=json.dumps(body.photos),
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _intern_to_out(obj)


@router.put("/internships/{item_id}", response_model=s.InternshipOut)
def update_internship(item_id: int, body: s.InternshipIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Internship).filter(m.Internship.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.company = body.company; obj.department = body.department
    obj.start_date = _parse_date(body.startDate); obj.end_date = _parse_date(body.endDate)
    obj.contribution = body.contribution; obj.photos = json.dumps(body.photos)
    db.commit(); db.refresh(obj)
    return _intern_to_out(obj)


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
