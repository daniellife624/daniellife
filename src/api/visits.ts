import type { VisitSummary } from '@/types/visits'
import { apiFetch } from './client'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
const SESSION_KEY = 'dl_visit_session'
const NO_TRACK_KEY = 'dl_no_track'

/** 登入過的裝置永久不記錄（避免把自己的瀏覽算進去） */
export function markNoTrack() {
  try { localStorage.setItem(NO_TRACK_KEY, '1') } catch { /* storage unavailable */ }
}

function isNoTrack(): boolean {
  try { return localStorage.getItem(NO_TRACK_KEY) === '1' } catch { return false }
}

/** 回傳 [sessionId, 是否為這個 session 的第一筆] */
function getSession(): [string, boolean] {
  try {
    const existing = sessionStorage.getItem(SESSION_KEY)
    if (existing) return [existing, false]
    const id = crypto.randomUUID()
    sessionStorage.setItem(SESSION_KEY, id)
    return [id, true]
  } catch {
    return [crypto.randomUUID(), true]
  }
}

export function trackVisit(path: string, src: string) {
  if (import.meta.env.DEV || isNoTrack()) return
  const [sessionId, isFirst] = getSession()
  // referrer 和 ?src 只在 session 第一筆送，之後站內換頁不算新的來源
  let referrer = ''
  if (isFirst && document.referrer) {
    try {
      if (new URL(document.referrer).host !== location.host) referrer = document.referrer.slice(0, 500)
    } catch { /* invalid referrer */ }
  }
  fetch(`${BASE_URL}/api/visits`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sessionId, path: path.slice(0, 200), referrer, src: isFirst ? src.slice(0, 50) : '' }),
    keepalive: true,
  }).catch(() => { /* 記錄失敗不影響瀏覽 */ })
}

export async function getVisitSummary(): Promise<VisitSummary> {
  return apiFetch<VisitSummary>('/api/visits/summary')
}
