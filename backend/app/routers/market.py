import asyncio
import time
from typing import Optional
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..config import settings

router = APIRouter(prefix="/market", tags=["market"])

# 國際指數（亞股/歐股/美股）：改用 Yahoo Finance v8 chart（單檔查詢）。
# 原本用的 v7/finance/quote 批次報價 API，Yahoo 已改成需要 crumb/cookie 驗證，
# 沒帶會直接回 401（不是偶爾被擋，是每次都失敗）；v8 chart 是圖表用途的端點，
# 目前仍可匿名逐檔查詢，改用這支並平行呼叫取代原本的單一批次請求。
_YF_SYMBOLS = [
    "^N225", "^KS11", "^HSI", "000001.SS",
    "^FTSE", "^GDAXI", "^FCHI", "^STOXX50E",
    "^GSPC", "^DJI", "^IXIC", "^RUT",
]
_YF_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
_YF_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://finance.yahoo.com/",
}


async def _fetch_yahoo_chart_quote(client: httpx.AsyncClient, symbol: str) -> Optional[dict]:
    try:
        res = await client.get(
            _YF_CHART_URL.format(symbol=symbol),
            params={"interval": "1d", "range": "2d"},
            headers=_YF_HEADERS,
        )
        res.raise_for_status()
        result = res.json().get("chart", {}).get("result") or []
        if not result:
            return None
        meta = result[0].get("meta", {})
        price = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        if price is None or prev is None:
            return None
        quote = result[0].get("indicators", {}).get("quote", [{}])[0]
        opens = [v for v in quote.get("open", []) if v is not None]
        return {
            "price": price,
            "change": price - prev,
            "changePct": (price - prev) / prev * 100 if prev else 0,
            "open": opens[-1] if opens else price,
            "high": meta.get("regularMarketDayHigh", price),
            "low": meta.get("regularMarketDayLow", price),
            "prev": prev,
        }
    except Exception:
        return None

# 台股：改用證交所官方即時行情 API（mis.twse.com.tw），不需金鑰、比 Yahoo 穩定非常多。
# ex_ch 代碼格式為 "{tse|otc}_{指數代碼}.tw"；t00=加權指數、o00=上櫃指數、t13=電子工業類指數、
# t17=金融保險類指數（實際測試過數字與 TWSE 官網一致）。
_TWSE_MIS_URL = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
_TWSE_CODES = {
    "tse_t00.tw": "^TWII",   # 加權指數
    "otc_o00.tw": "^TWO",    # 上櫃指數
    "tse_t13.tw": "TW_ELEC", # 電子類指數
    "tse_t17.tw": "TW_FIN",  # 金融類指數
}
_TWSE_HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


async def _fetch_twse_quotes(client: httpx.AsyncClient) -> dict:
    res = await client.get(_TWSE_MIS_URL, params={"ex_ch": "|".join(_TWSE_CODES)}, headers=_TWSE_HEADERS)
    res.raise_for_status()
    out: dict = {}
    for item in res.json().get("msgArray", []):
        sym = _TWSE_CODES.get(f"{item.get('ex')}_{item.get('ch')}")
        if not sym:
            continue

        def _num(key: str) -> Optional[float]:
            v = item.get(key)
            try:
                return float(v) if v and v != "-" else None
            except ValueError:
                return None

        prev = _num("y")
        price = _num("z") or prev
        if price is None or prev is None:
            continue
        out[sym] = {
            "price": price,
            "change": price - prev,
            "changePct": (price - prev) / prev * 100 if prev else 0,
            "open": _num("o") or price,
            "high": _num("h") or price,
            "low": _num("l") or price,
            "prev": prev,
        }
    return out


# Yahoo 對短時間內大量併發請求非常敏感——實測同時打 12 檔（asyncio.gather）幾乎每次
# 都會立刻被 429，且封鎖會持續一段時間（同一 IP 之後就算改成一次一檔也會繼續被擋）。
# 因此國際指數改成「逐檔依序查詢＋間隔」，並用 lock 確保 cache 過期時，多個同時湧入的
# request 只會有一個真的去打 Yahoo，其餘等待同一次結果，不會疊加成併發爆量。
# 失敗時優先回上一次成功的真實資料（即使有點舊），而不是直接掉回寫死很久沒更新的假資料。
_QUOTES_CACHE_TTL = 60  # 秒
_YF_REQUEST_GAP = 0.3   # 秒，逐檔查詢間隔
_quotes_cache: dict = {}
_quotes_cache_at: float = 0.0
_quotes_lock = asyncio.Lock()


@router.get("/quotes")
async def get_quotes():
    global _quotes_cache, _quotes_cache_at
    now = time.time()
    if _quotes_cache and (now - _quotes_cache_at) < _QUOTES_CACHE_TTL:
        return _quotes_cache

    async with _quotes_lock:
        now = time.time()
        if _quotes_cache and (now - _quotes_cache_at) < _QUOTES_CACHE_TTL:
            return _quotes_cache  # 等鎖的期間，已經有別的 request 刷新過 cache 了

        data: dict = {}
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            try:
                data.update(await _fetch_twse_quotes(client))
            except Exception:
                pass  # 台股取不到就先跳過，仍嘗試國際指數

            for sym in _YF_SYMBOLS:
                quote = await _fetch_yahoo_chart_quote(client, sym)
                if quote is not None:
                    data[sym] = quote
                await asyncio.sleep(_YF_REQUEST_GAP)

        if data:
            # 用合併而非整組覆蓋：這輪抓失敗的symbol，沿用上一次成功的舊資料，
            # 不會因為「台股成功、Yahoo 全部失敗」就把上一輪抓到的國際指數整組洗掉
            _quotes_cache = {**_quotes_cache, **data}
            _quotes_cache_at = now
            return _quotes_cache
        return _quotes_cache  # 這輪全部失敗才完全退回上一次成功的真實資料


_PROVIDERS: dict[str, dict] = {
    "gemini": {
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "token_key": "GEMINI_API_KEY",
        "model_key": "GEMINI_MODEL",
    },
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "token_key": "GROQ_API_KEY",
        "model_key": "GROQ_MODEL",
    },
    "github": {
        "url": "https://models.inference.ai.azure.com/chat/completions",
        "token_key": "GITHUB_TOKEN",
        "model_key": "GITHUB_MODELS_MODEL",
    },
}

_SYSTEM_PROMPT = (
    "你是「Daniellife 會計丹尼」個人網站的財經分析助手，"
    "幫助訪客理解財經市場動態、總體經濟新聞與投資概念。"
    "請用繁體中文簡潔清晰地回覆，重點以條列呈現。"
)

_PROVIDER_MODELS: dict[str, list[str]] = {
    "gemini": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
    "groq":   ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama-3.1-8b-instant"],
    "github": ["gpt-4o", "gpt-4o-mini", "Meta-Llama-3.3-70B-Instruct"],
}


class _ChatMsg(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[_ChatMsg]
    model: Optional[str] = None


@router.get("/chat/config")
def chat_config():
    provider = settings.AI_PROVIDER
    return {
        "provider": provider,
        "models": _PROVIDER_MODELS.get(provider, []),
        "default": getattr(settings, _PROVIDERS.get(provider, {}).get("model_key", ""), ""),
    }


@router.post("/chat")
async def chat(body: ChatRequest):
    provider = _PROVIDERS.get(settings.AI_PROVIDER)
    if not provider:
        raise HTTPException(503, f"不支援的 AI_PROVIDER：{settings.AI_PROVIDER}")

    token: str = getattr(settings, provider["token_key"], "")
    model: str = body.model or getattr(settings, provider["model_key"], "")
    if not token:
        raise HTTPException(503, f"AI 功能尚未設定（缺少 {provider['token_key']}）")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            *[m.model_dump() for m in body.messages],
        ],
        "max_tokens": 800,
        "temperature": 0.7,
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            res = await client.post(provider["url"], json=payload, headers=headers)
            res.raise_for_status()
            reply: str = res.json()["choices"][0]["message"]["content"]
            return {"reply": reply}
        except httpx.HTTPStatusError as e:
            raise HTTPException(502, f"AI 回應錯誤 ({settings.AI_PROVIDER}) {e.response.status_code}")
        except httpx.TimeoutException:
            raise HTTPException(504, "AI 請求逾時，請稍後再試")
        except Exception as e:
            raise HTTPException(502, f"AI 請求失敗：{e}")
