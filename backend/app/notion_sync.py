import re
import uuid
import html
from pathlib import Path
import httpx
from .config import settings

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

NOTE_IMG_DIR = Path(__file__).resolve().parent.parent / "uploads" / "thesis_notes"
NOTE_IMG_DIR.mkdir(parents=True, exist_ok=True)

_IMG_EXT_MAP = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}
_HEADING_TAG = {"heading_1": "h3", "heading_2": "h4", "heading_3": "h5"}


class NotionSyncError(Exception):
    pass


def extract_page_id(url: str) -> str:
    m = re.search(r'([0-9a-fA-F]{32})(?:[?#]|$)', url.replace('-', ''))
    if not m:
        raise NotionSyncError("無法從網址解析 Notion 頁面 ID，請確認貼的是完整頁面連結")
    hex_id = m.group(1)
    return f"{hex_id[0:8]}-{hex_id[8:12]}-{hex_id[12:16]}-{hex_id[16:20]}-{hex_id[20:32]}"


def _headers() -> dict:
    if not settings.NOTION_TOKEN:
        raise NotionSyncError("後端尚未設定 NOTION_TOKEN")
    return {
        "Authorization": f"Bearer {settings.NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
    }


def _fetch_blocks(client: httpx.Client, block_id: str) -> list[dict]:
    blocks: list[dict] = []
    cursor = None
    while True:
        params: dict = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        resp = client.get(f"{NOTION_API}/blocks/{block_id}/children", headers=_headers(), params=params)
        if resp.status_code != 200:
            raise NotionSyncError(f"Notion API 錯誤（{resp.status_code}）：{resp.text[:200]}")
        data = resp.json()
        blocks.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return blocks


def _rich_text_to_html(rich_text: list[dict]) -> str:
    parts = []
    for rt in rich_text:
        text = html.escape(rt.get("plain_text", ""))
        ann = rt.get("annotations", {})
        if ann.get("code"):
            text = f"<code>{text}</code>"
        if ann.get("bold"):
            text = f"<b>{text}</b>"
        if ann.get("italic"):
            text = f"<i>{text}</i>"
        if ann.get("strikethrough"):
            text = f"<s>{text}</s>"
        if ann.get("underline"):
            text = f"<u>{text}</u>"
        href = rt.get("href")
        if href:
            text = f'<a href="{html.escape(href)}" target="_blank" rel="noopener">{text}</a>'
        parts.append(text)
    return "".join(parts)


def _download_image(client: httpx.Client, url: str, paper_id: int) -> str | None:
    try:
        resp = client.get(url, timeout=20.0)
        resp.raise_for_status()
    except httpx.HTTPError:
        return None
    content_type = resp.headers.get("content-type", "image/png").split(";")[0]
    ext = _IMG_EXT_MAP.get(content_type, ".png")
    filename = f"{paper_id}_{uuid.uuid4().hex[:8]}{ext}"
    (NOTE_IMG_DIR / filename).write_bytes(resp.content)
    return f"/uploads/thesis_notes/{filename}"


def _blocks_to_html(client: httpx.Client, blocks: list[dict], paper_id: int) -> str:
    parts: list[str] = []
    list_stack: list[str] = []

    def close_lists():
        while list_stack:
            parts.append(f"</{list_stack.pop()}>")

    for block in blocks:
        btype = block.get("type", "")
        data = block.get(btype, {})

        if btype in ("bulleted_list_item", "numbered_list_item"):
            tag = "ul" if btype == "bulleted_list_item" else "ol"
            if not list_stack or list_stack[-1] != tag:
                close_lists()
                parts.append(f"<{tag}>")
                list_stack.append(tag)
            parts.append(f"<li>{_rich_text_to_html(data.get('rich_text', []))}</li>")
            continue
        close_lists()

        if btype == "paragraph":
            text = _rich_text_to_html(data.get("rich_text", []))
            if text:
                parts.append(f"<p>{text}</p>")
        elif btype in _HEADING_TAG:
            tag = _HEADING_TAG[btype]
            parts.append(f"<{tag}>{_rich_text_to_html(data.get('rich_text', []))}</{tag}>")
        elif btype in ("quote", "callout"):
            parts.append(f"<blockquote>{_rich_text_to_html(data.get('rich_text', []))}</blockquote>")
        elif btype == "code":
            code_text = html.escape("".join(rt.get("plain_text", "") for rt in data.get("rich_text", [])))
            parts.append(f"<pre><code>{code_text}</code></pre>")
        elif btype == "to_do":
            checked = "checked" if data.get("checked") else ""
            parts.append(f'<p><input type="checkbox" disabled {checked} /> {_rich_text_to_html(data.get("rich_text", []))}</p>')
        elif btype == "divider":
            parts.append("<hr />")
        elif btype == "image":
            src = (data.get("file") or {}).get("url") if data.get("type") == "file" else (data.get("external") or {}).get("url")
            if src:
                local_url = _download_image(client, src, paper_id)
                if local_url:
                    parts.append(f'<img src="{local_url}" style="max-width:100%;border-radius:4px;display:block;margin:8px 0;" />')
        # other block types (tables, embeds, etc.) are silently skipped

    close_lists()
    return "".join(parts)


PURPOSE_PROPERTY = "研究目的 (150)"
CONTRIBUTION_PROPERTY = "研究貢獻/影響/結果 (200)"


def _plain_text(prop: dict) -> str:
    return "".join(rt.get("plain_text", "") for rt in prop.get("rich_text", []))


def _fetch_page_properties(client: httpx.Client, page_id: str) -> dict:
    resp = client.get(f"{NOTION_API}/pages/{page_id}", headers=_headers())
    if resp.status_code != 200:
        raise NotionSyncError(f"Notion API 錯誤（{resp.status_code}）：{resp.text[:200]}")
    return resp.json().get("properties", {})


def sync_paper_notes(page_url: str, paper_id: int) -> dict:
    """回傳 {notes, purpose, contribution}：notes 為頁面本文轉 HTML，purpose/contribution 取自
    Notion 資料庫的「研究目的 (150)」「研究貢獻/影響/結果 (200)」欄位（取代原本手動輸入/LLM 生成的內容）。"""
    page_id = extract_page_id(page_url)
    with httpx.Client() as client:
        blocks = _fetch_blocks(client, page_id)
        notes = _blocks_to_html(client, blocks, paper_id)
        properties = _fetch_page_properties(client, page_id)
        purpose = _plain_text(properties.get(PURPOSE_PROPERTY, {}))
        contribution = _plain_text(properties.get(CONTRIBUTION_PROPERTY, {}))
        return {"notes": notes, "purpose": purpose, "contribution": contribution}
