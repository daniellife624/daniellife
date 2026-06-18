import type { NewsItem, NewsRegion } from '@/types/market'

const _news: NewsItem[] = [
  { id: 1, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'MSNBC', publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 2, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'CNN', publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 3, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC', publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 4, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC', publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 5, title: 'News Title', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: 'BBC', publishedAt: '2026/06/15 13:00', region: 'US' },
  { id: 6, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '經濟日報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
  { id: 7, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '工商時報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
  { id: 8, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '經濟日報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
  { id: 9, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '工商時報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
  { id: 10, title: '新聞標題', summary: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', source: '經濟日報', publishedAt: '2026/06/15 13:00', region: 'TAIWAN' },
]

export async function getNews(region: NewsRegion, page = 1, keyword = ''): Promise<{ items: NewsItem[]; total: number }> {
  // TODO: return apiFetch(`/api/news?tab=${region}&q=${keyword}&page=${page}`)
  const filtered = _news.filter(
    (n) => n.region === region && (!keyword || n.title.includes(keyword) || n.summary.includes(keyword)),
  )
  const pageSize = 5
  const start = (page - 1) * pageSize
  return { items: filtered.slice(start, start + pageSize), total: filtered.length }
}
