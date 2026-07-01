from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup

from ..database import get_db
from ..models.news import NewsCache

router = APIRouter(prefix="/api/news", tags=["news"])

ITIS_URL = "https://itisweb2.itis.org.tw/ITIS_Publish/ITISNews_New_One.asp"

CATEGORIES = {
    "cate1": "總體經濟",
    "cate2": "電子資訊",
    "cate3": "生技醫藥",
    "cate4": "化學民生",
    "cate6": "機械金屬能源",
}

CACHE_TTL_HOURS = 12


def _scrape_itis() -> list[dict]:
    r = requests.get(ITIS_URL, verify=False, timeout=15)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for cate_id, cate_name in CATEGORIES.items():
        anchor = soup.find("a", attrs={"name": cate_id})
        if not anchor:
            continue

        # The anchor lives in a <td>; its grandparent <tr> contains all news for this category
        td = anchor.find_parent("td")
        tr = td.find_parent("tr") if td else None
        if not tr:
            continue

        for a in tr.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if not href.startswith("http") or not text:
                continue
            results.append({
                "category": cate_id,
                "category_name": cate_name,
                "title": text,
                "url": href,
            })

    return results


def _is_cache_fresh(db: Session) -> bool:
    latest = db.query(NewsCache).order_by(NewsCache.fetched_at.desc()).first()
    if not latest:
        return False
    cutoff = datetime.now(timezone.utc) - timedelta(hours=CACHE_TTL_HOURS)
    fetched = latest.fetched_at
    if fetched.tzinfo is None:
        fetched = fetched.replace(tzinfo=timezone.utc)
    return fetched > cutoff


def _refresh_cache(db: Session) -> None:
    articles = _scrape_itis()
    db.query(NewsCache).delete()
    for art in articles:
        db.add(NewsCache(category=art["category"], title=art["title"], url=art["url"]))
    db.commit()


@router.get("/taiwan")
def get_taiwan_news(db: Session = Depends(get_db)):
    if not _is_cache_fresh(db):
        try:
            _refresh_cache(db)
        except Exception as e:
            # If scrape fails but we have stale cache, return it anyway
            rows = db.query(NewsCache).all()
            if rows:
                return _format_rows(rows)
            return {"error": str(e), "articles": []}

    rows = db.query(NewsCache).all()
    return _format_rows(rows)


def _format_rows(rows: list) -> dict:
    grouped: dict[str, list] = {}
    for row in rows:
        grouped.setdefault(row.category, []).append({
            "title": row.title,
            "url": row.url,
        })

    categories = []
    for cate_id, cate_name in CATEGORIES.items():
        if cate_id in grouped:
            categories.append({
                "id": cate_id,
                "name": cate_name,
                "articles": grouped[cate_id],
            })

    return {"categories": categories}
