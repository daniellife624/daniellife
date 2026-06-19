import type { NewsItem, NewsRegion } from '@/types/market'

// ── Guardian API (free, no auth required with test key) ──
const GUARDIAN_KEY = 'test'  // TODO: replace with real key from https://open-platform.theguardian.com/

function stripHtml(html: string): string {
  return html.replace(/<[^>]*>/g, '').replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&#x27;/g, "'")
}

async function fetchGuardian(
  region: NewsRegion,
  page: number,
  keyword: string,
): Promise<{ items: NewsItem[]; total: number }> {
  const baseQ = region === 'US'
    ? `economy finance${keyword ? ' ' + keyword : ''}`
    : `taiwan economy finance${keyword ? ' ' + keyword : ''}`

  const url =
    `https://content.guardianapis.com/search` +
    `?q=${encodeURIComponent(baseQ)}` +
    `&section=business` +
    `&order-by=newest` +
    `&page-size=5` +
    `&page=${page}` +
    `&show-fields=trailText` +
    `&api-key=${GUARDIAN_KEY}`

  const res = await fetch(url)
  if (!res.ok) throw new Error(`Guardian ${res.status}`)
  const json = await res.json()

  type GItem = { webTitle: string; webPublicationDate: string; webUrl: string; fields?: { trailText?: string } }
  const items: NewsItem[] = (json.response.results as GItem[]).map((r, i) => ({
    id: (page - 1) * 5 + i + 1,
    title: r.webTitle,
    summary: r.fields?.trailText ? stripHtml(r.fields.trailText) : '',
    source: region === 'US' ? 'The Guardian' : 'Guardian / TW',
    publishedAt: new Date(r.webPublicationDate).toLocaleString('zh-TW', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit',
    }),
    region,
    url: r.webUrl,
  }))

  // Cap total pages to 50 articles to avoid runaway pagination
  return { items, total: Math.min(json.response.total as number, 50) }
}

// ── Fallback mock data (used when Guardian API fails) ──
const _mockNews: NewsItem[] = [
  { id: 1, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'MSNBC', publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 2, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'CNN',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 3, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 4, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 5, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC',   publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 6, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '經濟日報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
  { id: 7, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '工商時報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
  { id: 8, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '經濟日報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
  { id: 9, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '工商時報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
  { id: 10, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '經濟日報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
]

export async function getNews(
  region: NewsRegion,
  page = 1,
  keyword = '',
): Promise<{ items: NewsItem[]; total: number }> {
  // US     → Guardian API (business section, economy/finance query)
  // TAIWAN → Guardian API with taiwan query (暫時方案)
  //          最終方案：資策會ITIS 每日產業新聞電子報
  //          https://itisweb2.itis.org.tw/ITIS_Publish/ITISNews_New_One.asp?td=YYYY/M/D
  //          回傳 HTML，需後端 proxy 解析後轉 JSON
  try {
    return await fetchGuardian(region, page, keyword)
  } catch {
    // API 失敗時 fallback 到 mock data
    const filtered = _mockNews.filter(
      n => n.region === region && (!keyword || n.title.includes(keyword) || n.summary.includes(keyword)),
    )
    const pageSize = 5
    const start = (page - 1) * pageSize
    return { items: filtered.slice(start, start + pageSize), total: filtered.length }
  }
}
