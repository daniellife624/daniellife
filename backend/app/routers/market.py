import re
from datetime import date, datetime
from typing import Optional
import httpx
from fastapi import APIRouter, HTTPException, Query
from bs4 import BeautifulSoup
from ..config import settings

router = APIRouter(prefix="/market", tags=["market"])

GUARDIAN_KEY = "test"
GUARDIAN_URL = "https://content.guardianapis.com/search"
PAGE_SIZE = 5

# Simple in-memory cache: { date_str: (fetched_at: datetime, items: list) }
_itis_cache: dict[str, tuple[datetime, list]] = {}
CACHE_TTL_SECONDS = 3600  # 1 hour


@router.get("/news")
async def get_news(
    region: str = Query("US", pattern="^(US|TAIWAN)$"),
    page: int = Query(1, ge=1),
    keyword: Optional[str] = Query(None),
):
    if region == "TAIWAN":
        return await _get_taiwan_news(page, keyword)
    return await _get_guardian_news(page, keyword)


async def _get_guardian_news(page: int, keyword: Optional[str]):
    params = {
        "api-key": GUARDIAN_KEY,
        "section": "business",
        "q": f"economy finance {keyword}" if keyword else "economy finance",
        "page": page,
        "page-size": PAGE_SIZE,
        "show-fields": "trailText",
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
    today = date.today()
    cache_key = today.isoformat()

    # Serve from cache if still fresh
    cached = _itis_cache.get(cache_key)
    if cached:
        fetched_at, all_items = cached
        if (datetime.now() - fetched_at).total_seconds() < CACHE_TTL_SECONDS:
            return _paginate(all_items, page, keyword)

    # Fetch fresh from ITIS
    url = f"{settings.ITIS_BASE_URL}?td={today.year}/{today.month}/{today.day}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
    }
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        try:
            res = await client.get(url, headers=headers)
            res.raise_for_status()

            # Detect encoding from header or meta tag
            encoding = _detect_encoding(res.content, res.headers.get("content-type", ""))
            html = res.content.decode(encoding, errors="replace")

            soup = BeautifulSoup(html, "html.parser")
            all_items = _parse_itis(soup, today.isoformat())

            # Store in cache
            _itis_cache[cache_key] = (datetime.now(), all_items)
            return _paginate(all_items, page, keyword)

        except httpx.TimeoutException:
            raise HTTPException(502, "ITIS request timed out")
        except httpx.HTTPStatusError as e:
            raise HTTPException(502, f"ITIS HTTP error {e.response.status_code}")
        except Exception as e:
            raise HTTPException(502, f"ITIS fetch failed: {e}")


_EVENT_KEYWORDS = ("研討會", "論壇", "工作坊", "說明會", "座談會", "線上課程", "訓練班", "報名")


def _paginate(items: list, page: int, keyword: Optional[str]) -> dict:
    # Exclude seminar/event-type items; keep only news articles
    items = [i for i in items if not any(k in i["title"] for k in _EVENT_KEYWORDS)]
    if keyword:
        kw = keyword.lower()
        items = [i for i in items if kw in i["title"].lower() or kw in i["summary"].lower()]
    start = (page - 1) * PAGE_SIZE
    return {"items": items[start: start + PAGE_SIZE], "total": len(items)}


def _detect_encoding(content: bytes, content_type: str) -> str:
    """Detect charset from Content-Type header or HTML meta tag."""
    m = re.search(r'charset=([^\s;]+)', content_type, re.I)
    if m:
        return m.group(1).strip('"\'')
    # Scan first 2KB for meta charset
    snippet = content[:2000].decode("ascii", errors="replace")
    m = re.search(r'charset=["\']?([a-zA-Z0-9\-]+)', snippet, re.I)
    if m:
        return m.group(1)
    return "utf-8"


def _parse_itis(soup: BeautifulSoup, published_at: str) -> list[dict]:
    """
    Parse ITIS news list page.
    Strategy: table cells first (ASP.NET table layout), fallback to all anchors.
    Filters: dedup by URL, skip nav/JS links, require title ≥ 8 chars.
    """
    seen: set[str] = set()
    items: list[dict] = []

    # Prefer links inside table cells; fall back to all anchors
    anchors = soup.select("table td a[href]") or soup.select("a[href]")

    skip_exts = {".css", ".js", ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc"}
    skip_prefixes = ("#", "javascript:", "mailto:", "tel:")

    for tag in anchors:
        title = tag.get_text(strip=True)
        href = tag.get("href", "").strip()

        if not title or len(title) < 8:
            continue
        if any(href.startswith(p) for p in skip_prefixes):
            continue
        if any(href.lower().endswith(e) for e in skip_exts):
            continue

        # Normalize to absolute URL
        if href.startswith("http"):
            full_url = href
        elif href.startswith("/"):
            full_url = f"https://itisweb2.itis.org.tw{href}"
        else:
            full_url = f"https://itisweb2.itis.org.tw/ITIS_Publish/{href}"

        if full_url in seen:
            continue
        seen.add(full_url)

        # Try to extract summary from nearest td/li/div container
        summary = _extract_summary(tag, title)

        items.append({
            "id": full_url,
            "title": title,
            "summary": summary,
            "url": full_url,
            "publishedAt": published_at,
            "source": "ITIS 資策會",
        })

    return items


def _extract_summary(tag, title: str) -> str:
    """Get surrounding text from the nearest block container, minus the title."""
    for selector in ("td", "li", "div", "p"):
        container = tag.find_parent(selector)
        if container:
            text = container.get_text(" ", strip=True)
            extra = text.replace(title, "", 1).strip(" ·-–—|")
            if 10 < len(extra) < 300:
                return extra
    return ""
