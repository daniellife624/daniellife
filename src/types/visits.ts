export interface PeriodStats {
  views: number
  sessions: number
  visitors: number
}

export interface VisitSession {
  sessionId: string
  startedAt: string
  lastAt: string
  source: string
  device: string
  browser: string
  pages: string[]
  views: number
  returning: boolean
}

export interface VisitSummary {
  totals: { today: PeriodStats; last7: PeriodStats; last30: PeriodStats; all: PeriodStats }
  sources: { source: string; sessions: number }[]
  recent: VisitSession[]
}
