from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests

from ..database import get_db
from ..models.news import NewsCache

router = APIRouter(prefix="/api/news", tags=["news"])

# 原本抓的 ITIS 頁面（ITISNews_New_One.asp）已被官網改版拿掉，「每日新聞」被收進
# 會員專區、不再對外公開，整個頁面回 404，不是暫時性故障，救不回來（2026-08-23）。
# 改用鉅亨網（cnyes）的公開新聞 API（沒有官方文件、不需金鑰，是他們自家前端在用的
# 內部 API，穩定性沒有官方保證，但目前測試可正常運作）。
#
# cnyes 是市場別（台股/國際股市/科技…）分類，不是 ITIS 原本的產業別（電子資訊/生技
# 醫藥/化學民生/機械金屬能源）分類，兩者無法一一對應；且前端 market.ts 的
# TAIWAN_CATES 本來就只實際顯示 cate1（總體經濟）、cate2（電子資訊）兩類，所以只保留
# 這兩類，改用 cnyes 最接近的分類，其餘（生技醫藥/化學民生/機械金屬能源）不再提供。
CATEGORIES = {
    "cate1": "總體經濟",
    "cate2": "電子資訊",
}
_CNYES_SLUGS = {
    "cate1": "tw_macro",
    "cate2": "tech",
}
_CNYES_LIST_URL = "https://api.cnyes.com/media/api/v1/newslist/category/{slug}"
_CNYES_ARTICLE_URL = "https://news.cnyes.com/news/id/{news_id}"

CACHE_TTL_HOURS = 12


def _scrape_cnyes() -> list[dict]:
    results = []
    for cate_id, slug in _CNYES_SLUGS.items():
        r = requests.get(_CNYES_LIST_URL.format(slug=slug), params={"limit": 20}, timeout=15)
        r.raise_for_status()
        for item in r.json().get("items", {}).get("data", []):
            news_id = item.get("newsId")
            title = item.get("title")
            if not news_id or not title:
                continue
            results.append({
                "category": cate_id,
                "category_name": CATEGORIES[cate_id],
                "title": title,
                "url": _CNYES_ARTICLE_URL.format(news_id=news_id),
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
    articles = _scrape_cnyes()
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
