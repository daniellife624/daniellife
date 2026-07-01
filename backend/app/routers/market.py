from typing import Optional
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..config import settings

router = APIRouter(prefix="/market", tags=["market"])


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
