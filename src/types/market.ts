export type NewsRegion = 'US' | 'TAIWAN'

export interface NewsItem {
  id: number
  title: string
  summary: string
  source: string
  publishedAt: string
  region: NewsRegion
  url?: string
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}
