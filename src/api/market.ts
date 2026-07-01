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
const TAIWAN_CATES = new Set(['cate1', 'cate2'])

async function fetchTaiwanNews(page: number, keyword: string): Promise<{ items: NewsItem[]; total: number }> {
  const data = await apiFetch<{
    categories: { id: string; name: string; articles: { title: string; url: string }[] }[]
  }>('/api/news/taiwan')

  const all: NewsItem[] = []
  let idx = 1
  for (const cat of data.categories) {
    if (!TAIWAN_CATES.has(cat.id)) continue
    for (const art of cat.articles) {
      if (keyword && !art.title.includes(keyword)) continue
      all.push({
        id: idx++,
        title: art.title,
        summary: '',
        source: cat.name,
        publishedAt: '',
        region: 'TAIWAN',
        url: art.url,
      })
    }
  }

  const PAGE_SIZE = 5
  const start = (page - 1) * PAGE_SIZE
  return { items: all.slice(start, start + PAGE_SIZE), total: all.length }
}

// ── Fallback mock (Guardian fails) ──
const _mockUS: NewsItem[] = [
  { id: 1, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'MSNBC', publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 2, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'CNN',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 3, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 4, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 5, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC',   publishedAt: '2026/06/15 13:00', region: 'US' },
]

export async function getChatConfig(): Promise<{ provider: string; models: string[]; default: string }> {
  return apiFetch('/api/market/chat/config')
}

export async function sendChatMessage(messages: ChatMessage[], model?: string): Promise<string> {
  const data = await apiFetch<{ reply: string }>('/api/market/chat', {
    method: 'POST',
    body: JSON.stringify({ messages, model }),
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
