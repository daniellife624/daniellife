import hashlib
import re
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..deps import get_current_user
from ..models.visit import PageView
from ..schemas.visits import VisitIn, VisitSummary, VisitTotals, PeriodStats, SourceCount, SessionOut

router = APIRouter(prefix="/visits", tags=["visits"])

TAIPEI = timezone(timedelta(hours=8))
RECENT_SESSIONS = 50

_BOT_RE = re.compile(r"bot|crawl|spider|slurp|preview|headless|lighthouse|python-requests|curl|wget", re.I)

# ?src= 參數（分享連結時自己加的）→ 顯示名稱
_SRC_LABELS = {"104": "104", "linkedin": "LinkedIn", "li": "LinkedIn", "cake": "Cake", "resume": "履歷 PDF"}

# referrer 網域 → 顯示名稱
_REFERRER_LABELS = [
    ("linkedin.com", "LinkedIn"), ("lnkd.in", "LinkedIn"),
    ("104.com.tw", "104"),
    ("google.", "Google"), ("bing.com", "Bing"),
    ("facebook.com", "Facebook"), ("instagram.com", "Instagram"),
    ("github.com", "GitHub"), ("cake.me", "Cake"),
]

# 簡單的 rate limit：同一訪客每分鐘最多 30 筆，避免公開端點被灌資料
_RATE_LIMIT = 30
_recent_hits: dict[str, deque[float]] = defaultdict(deque)


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else ""


def _device(ua: str) -> str:
    if re.search(r"iPad|Tablet", ua):
        return "平板"
    if re.search(r"Mobi|Android|iPhone", ua):
        return "手機"
    return "電腦"


def _browser(ua: str) -> str:
    for pattern, label in [
        (r"LinkedInApp", "LinkedIn App"), (r"FBAN|FBAV", "Facebook App"), (r"Instagram", "Instagram App"),
        (r"\bLine/", "LINE"), (r"Edg/", "Edge"), (r"OPR/", "Opera"), (r"SamsungBrowser", "Samsung"),
        (r"CriOS|Chrome/", "Chrome"), (r"FxiOS|Firefox/", "Firefox"), (r"Safari/", "Safari"),
    ]:
        if re.search(pattern, ua):
            return label
    return "其他"


def _source(src: str, referrer: str, browser: str) -> str:
    src = src.strip()
    if src:
        return _SRC_LABELS.get(src.lower(), src[:50])
    host = (urlparse(referrer).hostname or "").lower()
    for key, label in _REFERRER_LABELS:
        if key in host:
            return label
    if host:
        return host[:50]
    # LinkedIn App 內建瀏覽器常常不帶 referrer，用 UA 補判斷
    if browser == "LinkedIn App":
        return "LinkedIn"
    return "直接開啟"


def _rate_limited(key: str) -> bool:
    now = time.monotonic()
    hits = _recent_hits[key]
    while hits and now - hits[0] > 60:
        hits.popleft()
    if len(hits) >= _RATE_LIMIT:
        return True
    hits.append(now)
    if len(_recent_hits) > 5000:   # 防止記憶體無限成長
        _recent_hits.clear()
    return False


@router.post("", status_code=204)
def record_visit(body: VisitIn, request: Request, db: Session = Depends(get_db)):
    ua = request.headers.get("user-agent", "")[:500]
    if not ua or _BOT_RE.search(ua):
        return Response(status_code=204)

    visitor_hash = hashlib.sha256(f"{_client_ip(request)}|{ua}|{settings.SECRET_KEY}".encode()).hexdigest()[:16]
    if _rate_limited(visitor_hash):
        return Response(status_code=204)

    browser = _browser(ua)
    db.add(PageView(
        visited_at=datetime.now(timezone.utc).replace(tzinfo=None),
        session_id=body.sessionId,
        visitor_hash=visitor_hash,
        path=body.path,
        source=_source(body.src, body.referrer, browser),
        referrer=body.referrer,
        device=_device(ua),
        browser=browser,
    ))
    db.commit()
    return Response(status_code=204)


def _period_stats(db: Session, since: datetime | None) -> PeriodStats:
    q = db.query(
        func.count(PageView.id),
        func.count(func.distinct(PageView.session_id)),
        func.count(func.distinct(PageView.visitor_hash)),
    )
    if since is not None:
        q = q.filter(PageView.visited_at >= since)
    views, sessions, visitors = q.one()
    return PeriodStats(views=views, sessions=sessions, visitors=visitors)


def _iso(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


@router.get("/summary", response_model=VisitSummary)
def visit_summary(db: Session = Depends(get_db), _=Depends(get_current_user)):
    now_utc = datetime.now(timezone.utc)
    today_start = now_utc.astimezone(TAIPEI).replace(hour=0, minute=0, second=0, microsecond=0)
    to_utc = lambda dt: dt.astimezone(timezone.utc).replace(tzinfo=None)  # noqa: E731
    since_30 = to_utc(now_utc - timedelta(days=30))

    totals = VisitTotals(
        today=_period_stats(db, to_utc(today_start)),
        last7=_period_stats(db, to_utc(now_utc - timedelta(days=7))),
        last30=_period_stats(db, since_30),
        all=_period_stats(db, None),
    )

    # 近 30 天各來源的 session 數（以 session 第一筆的來源為準）
    rows = db.query(PageView).filter(PageView.visited_at >= since_30).order_by(PageView.visited_at).all()
    first_source: dict[str, str] = {}
    for r in rows:
        first_source.setdefault(r.session_id, r.source)
    source_counts: dict[str, int] = defaultdict(int)
    for s in first_source.values():
        source_counts[s] += 1
    sources = [SourceCount(source=s, sessions=n) for s, n in sorted(source_counts.items(), key=lambda x: -x[1])]

    # 最近的 session
    recent_ids = [
        sid for (sid,) in db.query(PageView.session_id)
        .group_by(PageView.session_id)
        .order_by(func.max(PageView.visited_at).desc())
        .limit(RECENT_SESSIONS)
    ]
    views = (
        db.query(PageView).filter(PageView.session_id.in_(recent_ids)).order_by(PageView.visited_at).all()
        if recent_ids else []
    )
    by_session: dict[str, list[PageView]] = defaultdict(list)
    for v in views:
        by_session[v.session_id].append(v)

    # 每個訪客第一次出現的 session，用來判斷是不是回訪
    hashes = {v.visitor_hash for v in views}
    first_session_of: dict[str, str] = {}
    if hashes:
        for vh, sid in (
            db.query(PageView.visitor_hash, PageView.session_id)
            .filter(PageView.visitor_hash.in_(hashes))
            .order_by(PageView.visited_at)
        ):
            first_session_of.setdefault(vh, sid)

    recent = []
    for sid in recent_ids:
        pvs = by_session[sid]
        first, last = pvs[0], pvs[-1]
        pages = list(dict.fromkeys(p.path for p in pvs))   # 去重但保留順序
        recent.append(SessionOut(
            sessionId=sid, startedAt=_iso(first.visited_at), lastAt=_iso(last.visited_at),
            source=first.source, device=first.device, browser=first.browser,
            pages=pages, views=len(pvs), returning=first_session_of.get(first.visitor_hash) != sid,
        ))

    return VisitSummary(totals=totals, sources=sources, recent=recent)
