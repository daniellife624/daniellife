from datetime import date
from typing import Optional
import httpx
from fastapi import APIRouter, HTTPException, Query
from bs4 import BeautifulSoup
from ..config import settings

router = APIRouter(prefix="/market", tags=["market"])

GUARDIAN_KEY = "test"
GUARDIAN_URL = "https://content.guardianapis.com/search"
PAGE_SIZE = 5


@router.get("/news")
async def get_news(
    region: str = Query("US", pattern="^(US|TAIWAN)$"),
    page: int = Query(1, ge=1),
    keyword: Optional[str] = Query(None),
):
    if region == "TAIWAN":
        return await _get_taiwan_news(page, keyword)
    return await _get_guardian_news(page, keyword, section="business", q="economy finance")


async def _get_guardian_news(page: int, keyword: Optional[str], section: str, q: str):
    params = {
        "api-key": GUARDIAN_KEY,
        "section": section,
        "q": f"{q} {keyword}" if keyword else q,
        "page": page,
        "page-size": PAGE_SIZE,
        "show-fields": "trailText,byline,thumbnail",
        "order-by": "newest",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            res = await client.get(GUARDIAN_URL, params=params)
            res.raise_for_status()
            data = res.json()["response"]
            items = [
                {
                    "id": r["id"],
                    "title": r["webTitle"],
                    "summary": (r.get("fields") or {}).get("trailText", ""),
                    "url": r["webUrl"],
                    "publishedAt": r["webPublicationDate"],
                    "source": "The Guardian",
                }
                for r in data["results"]
            ]
            return {"items": items, "total": min(data["total"], 50)}
        except Exception:
            return {"items": [], "total": 0}


async def _get_taiwan_news(page: int, keyword: Optional[str]):
    # ITIS proxy: fetch HTML and parse news list
    today = date.today()
    url = f"{settings.ITIS_BASE_URL}?td={today.year}/{today.month}/{today.day}"
    async with httpx.AsyncClient(timeout=15, follow_redirects=True, headers={
        "User-Agent": "Mozilla/5.0 (compatible; Daniellife/1.0)"
    }) as client:
        try:
            res = await client.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            items = _parse_itis(soup, today.isoformat())
            # Client-side keyword filter
            if keyword:
                kw = keyword.lower()
                items = [i for i in items if kw in i["title"].lower() or kw in i["summary"].lower()]
            start = (page - 1) * PAGE_SIZE
            return {"items": items[start: start + PAGE_SIZE], "total": len(items)}
        except Exception as e:
            raise HTTPException(502, f"ITIS fetch failed: {e}")


def _parse_itis(soup: BeautifulSoup, published_at: str) -> list[dict]:
    items = []
    for tag in soup.select("a[href]"):
        title = tag.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        href = tag["href"]
        if "ITIS" not in href and "itis" not in href:
            continue
        items.append({
            "id": href,
            "title": title,
            "summary": "",
            "url": href if href.startswith("http") else f"https://itisweb2.itis.org.tw{href}",
            "publishedAt": published_at,
            "source": "ITIS 資策會",
        })
    return items
