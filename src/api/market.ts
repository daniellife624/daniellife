import type { NewsItem, NewsRegion, ChatMessage } from '@/types/market'
import { apiFetch } from './client'

// ── Guardian API (free test key) ──
const GUARDIAN_KEY = 'test'

function stripHtml(html: string): string {
  return html.replace(/<[^>]*>/g, '').replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&#x27;/g, "'")
}

async function fetchGuardian(page: number, keyword: string): Promise<{ items: NewsItem[]; total: number }> {
  const q = `economy finance${keyword ? ' ' + keyword : ''}`
  const url =
    `https://content.guardianapis.com/search` +
    `?q=${encodeURIComponent(q)}&section=business&order-by=newest` +
    `&page-size=5&page=${page}&show-fields=trailText&api-key=${GUARDIAN_KEY}`

  const res = await fetch(url)
  if (!res.ok) throw new Error(`Guardian ${res.status}`)
  const json = await res.json()

  type GItem = { webTitle: string; webPublicationDate: string; webUrl: string; fields?: { trailText?: string } }
  const items: NewsItem[] = (json.response.results as GItem[]).map((r, i) => ({
    id: (page - 1) * 5 + i + 1,
    title: r.webTitle,
    summary: r.fields?.trailText ? stripHtml(r.fields.trailText) : '',
    source: 'The Guardian',
    publishedAt: new Date(r.webPublicationDate).toLocaleString('zh-TW', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit',
    }),
    region: 'US',
    url: r.webUrl,
  }))

  return { items, total: Math.min(json.response.total as number, 50) }
}

// ── ITIS backend proxy (TAIWAN) ──
async function fetchTaiwanNews(page: number, keyword: string): Promise<{ items: NewsItem[]; total: number }> {
  const params = new URLSearchParams({ region: 'TAIWAN', page: String(page) })
  if (keyword) params.set('keyword', keyword)
  const data = await apiFetch<{ items: Array<{ id: string; title: string; summary: string; url: string; publishedAt: string; source: string }>; total: number }>(
    `/api/market/news?${params}`
  )
  const items: NewsItem[] = data.items.map((r, i) => ({
    id: (page - 1) * 5 + i + 1,
    title: r.title,
    summary: r.summary,
    source: r.source,
    publishedAt: r.publishedAt,
    region: 'TAIWAN',
    url: r.url,
  }))
  return { items, total: data.total }
}

// ── Fallback mock (Guardian fails) ──
const _mockUS: NewsItem[] = [
  { id: 1, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'MSNBC', publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 2, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'CNN',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 3, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 4, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 5, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC',   publishedAt: '2026/06/15 13:00', region: 'US' },
]

export async function sendChatMessage(messages: ChatMessage[]): Promise<string> {
  const data = await apiFetch<{ reply: string }>('/api/market/chat', {
    method: 'POST',
    body: JSON.stringify({ messages }),
  })
  return data.reply
}

export async function getNews(
  region: NewsRegion,
  page = 1,
  keyword = '',
): Promise<{ items: NewsItem[]; total: number }> {
  if (region === 'TAIWAN') {
    try {
      return await fetchTaiwanNews(page, keyword)
    } catch {
      return { items: [], total: 0 }
    }
  }

  // US → Guardian API
  try {
    return await fetchGuardian(page, keyword)
  } catch {
    const start = (page - 1) * 5
    return { items: _mockUS.slice(start, start + 5), total: _mockUS.length }
  }
}
