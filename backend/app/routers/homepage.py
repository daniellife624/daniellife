import json
import uuid
from datetime import date
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from ..models import homepage as m
from ..schemas import homepage as s

INTERN_UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads" / "internships"
INTERN_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE_MB = 10

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


def _parse_period(period: str):
    sep = "–" if "–" in period else "-"
    parts = [p.strip() for p in period.split(sep, 1)]
    start = _parse_date(parts[0])
    end = None
    if len(parts) > 1 and parts[1] not in ("至今", "present", "now", ""):
        end = _parse_date(parts[1])
    return start, end


def _fmt_period(start: date | None, end: date | None) -> str:
    if start is None:
        return ""
    fmt = start.strftime("%Y/%m")
    return f"{fmt} – {end.strftime('%Y/%m')}" if end else f"{fmt} – 至今"


def _intern_out(r: m.Internship) -> s.InternshipOut:
    return s.InternshipOut(
        id=r.id, company=r.company, dept=r.dept, role=r.role,
        period=_fmt_period(r.start_date, r.end_date),
        contribution=r.contribution, photoUrl=r.photo_url,
    )


def _project_out(r: m.Project) -> s.ProjectOut:
    return s.ProjectOut(
        id=r.id, name=r.name, type=r.type,
        techLabel=r.tech_label, tech=r.tech,
        members=r.members, period=r.period, core=r.core,
        githubUrl=r.github_url, youtubeUrl=r.youtube_url,
        star=json.loads(r.star) if r.star else [],
        createdAt=r.created_at,
    )


# ── Internships ──────────────────────────────────────────────────
@router.get("/internships", response_model=list[s.InternshipOut])
def list_internships(db: Session = Depends(get_db)):
    return [_intern_out(r) for r in db.query(m.Internship).all()]


@router.post("/internships", response_model=s.InternshipOut)
def create_internship(body: s.InternshipIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    start, end = _parse_period(body.period)
    obj = m.Internship(
        company=body.company, dept=body.dept, role=body.role,
        start_date=start, end_date=end,
        contribution=body.contribution, photo_url=body.photoUrl,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _intern_out(obj)


@router.put("/internships/{item_id}", response_model=s.InternshipOut)
def update_internship(item_id: int, body: s.InternshipIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Internship).filter(m.Internship.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    start, end = _parse_period(body.period)
    obj.company = body.company; obj.dept = body.dept; obj.role = body.role
    obj.start_date = start; obj.end_date = end
    obj.contribution = body.contribution; obj.photo_url = body.photoUrl
    db.commit(); db.refresh(obj)
    return _intern_out(obj)


@router.delete("/internships/{item_id}", status_code=204)
def delete_internship(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Internship).filter(m.Internship.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


@router.post("/internships/{item_id}/photo", response_model=s.InternshipOut)
async def upload_internship_photo(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    obj = db.query(m.Internship).filter(m.Internship.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"不支援的檔案類型：{file.content_type}")
    content = await file.read()
    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, f"檔案大小超過 {MAX_SIZE_MB}MB 限制")
    ext = Path(file.filename or "photo.jpg").suffix.lower() or ".jpg"
    filename = f"{item_id}_{uuid.uuid4().hex[:8]}{ext}"
    (INTERN_UPLOAD_DIR / filename).write_bytes(content)
    if obj.photo_url:
        old = INTERN_UPLOAD_DIR / Path(obj.photo_url).name
        if old.exists():
            old.unlink()
    obj.photo_url = f"/uploads/internships/{filename}"
    db.commit(); db.refresh(obj)
    return _intern_out(obj)


@router.delete("/internships/{item_id}/photo", response_model=s.InternshipOut)
def delete_internship_photo(
    item_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    obj = db.query(m.Internship).filter(m.Internship.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    if obj.photo_url:
        target = INTERN_UPLOAD_DIR / Path(obj.photo_url).name
        if target.exists():
            target.unlink()
    obj.photo_url = None
    db.commit(); db.refresh(obj)
    return _intern_out(obj)


# ── Projects ─────────────────────────────────────────────────────
@router.get("/projects", response_model=list[s.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return [_project_out(r) for r in db.query(m.Project).order_by(m.Project.created_at.desc()).all()]


@router.post("/projects", response_model=s.ProjectOut)
def create_project(body: s.ProjectIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.Project(
        name=body.name, type=body.type, tech_label=body.techLabel,
        tech=body.tech, members=body.members, period=body.period,
        core=body.core, github_url=body.githubUrl, youtube_url=body.youtubeUrl,
        star=json.dumps([item.model_dump() for item in body.star], ensure_ascii=False),
        created_at=body.createdAt,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _project_out(obj)


@router.put("/projects/{item_id}", response_model=s.ProjectOut)
def update_project(item_id: int, body: s.ProjectIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Project).filter(m.Project.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.name = body.name; obj.type = body.type; obj.tech_label = body.techLabel
    obj.tech = body.tech; obj.members = body.members; obj.period = body.period
    obj.core = body.core; obj.github_url = body.githubUrl; obj.youtube_url = body.youtubeUrl
    obj.star = json.dumps([item.model_dump() for item in body.star], ensure_ascii=False)
    obj.created_at = body.createdAt
    db.commit(); db.refresh(obj)
    return _project_out(obj)


@router.delete("/projects/{item_id}", status_code=204)
def delete_project(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.Project).filter(m.Project.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Certs (public) ────────────────────────────────────────────────
@router.get("/certs", response_model=s.CertDataOut)
def get_certs(db: Session = Depends(get_db)):
    lang_en = [s.LangCertOut(name=r.name, score=r.score, pct=r.pct)
               for r in db.query(m.LanguageCert).filter(m.LanguageCert.lang == "en").all()]
    lang_jp = [s.LangCertOut(name=r.name, score=r.score, pct=r.pct)
               for r in db.query(m.LanguageCert).filter(m.LanguageCert.lang == "jp").all()]
    finance = [s.CertGroupOut(category=r.category, items=json.loads(r.items) if r.items else [])
               for r in db.query(m.CertGroup).filter(m.CertGroup.domain == "finance").order_by(m.CertGroup.sort_order).all()]
    it = [s.CertGroupOut(category=r.category, items=json.loads(r.items) if r.items else [])
          for r in db.query(m.CertGroup).filter(m.CertGroup.domain == "it").order_by(m.CertGroup.sort_order).all()]
    return s.CertDataOut(language=s.LanguageData(en=lang_en, jp=lang_jp), finance=finance, it=it)


# ── Lang Certs (admin CRUD) ───────────────────────────────────────
def _lang_cert_out(r: m.LanguageCert) -> s.LangCertAdminOut:
    return s.LangCertAdminOut(id=r.id, lang=r.lang, name=r.name, score=r.score, pct=r.pct)


@router.get("/lang-certs", response_model=list[s.LangCertAdminOut])
def list_lang_certs(db: Session = Depends(get_db)):
    return [_lang_cert_out(r) for r in db.query(m.LanguageCert).all()]


@router.post("/lang-certs", response_model=s.LangCertAdminOut)
def create_lang_cert(body: s.LangCertIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.LanguageCert(lang=body.lang, name=body.name, score=body.score, pct=body.pct)
    db.add(obj); db.commit(); db.refresh(obj)
    return _lang_cert_out(obj)


@router.put("/lang-certs/{item_id}", response_model=s.LangCertAdminOut)
def update_lang_cert(item_id: int, body: s.LangCertIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.LanguageCert).filter(m.LanguageCert.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.lang = body.lang; obj.name = body.name; obj.score = body.score; obj.pct = body.pct
    db.commit(); db.refresh(obj)
    return _lang_cert_out(obj)


@router.delete("/lang-certs/{item_id}", status_code=204)
def delete_lang_cert(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.LanguageCert).filter(m.LanguageCert.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Cert Groups (admin CRUD) ──────────────────────────────────────
def _cert_group_out(r: m.CertGroup) -> s.CertGroupAdminOut:
    return s.CertGroupAdminOut(
        id=r.id, domain=r.domain, category=r.category,
        items=json.loads(r.items) if r.items else [],
        sortOrder=r.sort_order,
    )


@router.get("/cert-groups", response_model=list[s.CertGroupAdminOut])
def list_cert_groups(db: Session = Depends(get_db)):
    return [_cert_group_out(r) for r in db.query(m.CertGroup).order_by(m.CertGroup.sort_order).all()]


@router.post("/cert-groups", response_model=s.CertGroupAdminOut)
def create_cert_group(body: s.CertGroupIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.CertGroup(
        domain=body.domain, category=body.category,
        items=json.dumps(body.items, ensure_ascii=False), sort_order=body.sortOrder,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return _cert_group_out(obj)


@router.put("/cert-groups/{item_id}", response_model=s.CertGroupAdminOut)
def update_cert_group(item_id: int, body: s.CertGroupIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.CertGroup).filter(m.CertGroup.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.domain = body.domain; obj.category = body.category
    obj.items = json.dumps(body.items, ensure_ascii=False); obj.sort_order = body.sortOrder
    db.commit(); db.refresh(obj)
    return _cert_group_out(obj)


@router.delete("/cert-groups/{item_id}", status_code=204)
def delete_cert_group(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.CertGroup).filter(m.CertGroup.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── Academic ─────────────────────────────────────────────────────
@router.get("/academic", response_model=list[s.AcademicMilestoneOut])
def list_academic(db: Session = Depends(get_db)):
    rows = db.query(m.AcademicMilestone).order_by(m.AcademicMilestone.sort_order).all()
    return [s.AcademicMilestoneOut(
        id=r.id, school=r.school, major=r.major, period=r.period,
        gpa=r.gpa, rank=r.rank, facts=json.loads(r.facts) if r.facts else [],
        sortOrder=r.sort_order,
    ) for r in rows]


@router.post("/academic", response_model=s.AcademicMilestoneOut)
def create_academic(body: s.AcademicMilestoneIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.AcademicMilestone(
        school=body.school, major=body.major, period=body.period,
        gpa=body.gpa, rank=body.rank,
        facts=json.dumps(body.facts, ensure_ascii=False), sort_order=body.sortOrder,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return s.AcademicMilestoneOut(
        id=obj.id, school=obj.school, major=obj.major, period=obj.period,
        gpa=obj.gpa, rank=obj.rank, facts=json.loads(obj.facts), sortOrder=obj.sort_order,
    )


@router.put("/academic/{item_id}", response_model=s.AcademicMilestoneOut)
def update_academic(item_id: int, body: s.AcademicMilestoneIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.AcademicMilestone).filter(m.AcademicMilestone.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.school = body.school; obj.major = body.major; obj.period = body.period
    obj.gpa = body.gpa; obj.rank = body.rank
    obj.facts = json.dumps(body.facts, ensure_ascii=False); obj.sort_order = body.sortOrder
    db.commit(); db.refresh(obj)
    return s.AcademicMilestoneOut(
        id=obj.id, school=obj.school, major=obj.major, period=obj.period,
        gpa=obj.gpa, rank=obj.rank, facts=json.loads(obj.facts), sortOrder=obj.sort_order,
    )


@router.delete("/academic/{item_id}", status_code=204)
def delete_academic(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.AcademicMilestone).filter(m.AcademicMilestone.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()


# ── FuturePlan ───────────────────────────────────────────────────
@router.get("/future-plans", response_model=list[s.FuturePlanOut])
def list_future_plans(db: Session = Depends(get_db)):
    rows = db.query(m.FuturePlan).order_by(m.FuturePlan.sort_order).all()
    return [s.FuturePlanOut(
        id=r.id, phase=r.phase, title=r.title, subtitle=r.subtitle,
        items=json.loads(r.items) if r.items else [], sortOrder=r.sort_order,
    ) for r in rows]


@router.post("/future-plans", response_model=s.FuturePlanOut)
def create_future_plan(body: s.FuturePlanIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = m.FuturePlan(
        phase=body.phase, title=body.title, subtitle=body.subtitle,
        items=json.dumps(body.items, ensure_ascii=False), sort_order=body.sortOrder,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return s.FuturePlanOut(id=obj.id, phase=obj.phase, title=obj.title, subtitle=obj.subtitle, items=json.loads(obj.items), sortOrder=obj.sort_order)


@router.put("/future-plans/{item_id}", response_model=s.FuturePlanOut)
def update_future_plan(item_id: int, body: s.FuturePlanIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.FuturePlan).filter(m.FuturePlan.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    obj.phase = body.phase; obj.title = body.title; obj.subtitle = body.subtitle
    obj.items = json.dumps(body.items, ensure_ascii=False); obj.sort_order = body.sortOrder
    db.commit(); db.refresh(obj)
    return s.FuturePlanOut(id=obj.id, phase=obj.phase, title=obj.title, subtitle=obj.subtitle, items=json.loads(obj.items), sortOrder=obj.sort_order)


@router.delete("/future-plans/{item_id}", status_code=204)
def delete_future_plan(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = db.query(m.FuturePlan).filter(m.FuturePlan.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj); db.commit()
