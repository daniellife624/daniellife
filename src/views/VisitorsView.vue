<template>
  <div class="visitors">
    <div class="visitors__inner">
      <p v-if="error" class="visitors__error">{{ error }}</p>

      <template v-if="summary">
        <div class="metric-cards">
          <div v-for="p in periods" :key="p.key" class="metric-card">
            <p class="metric-card__label">{{ p.label }}</p>
            <p class="metric-card__value">{{ summary.totals[p.key].sessions }} <span class="metric-card__unit">次造訪</span></p>
            <p class="metric-card__sub">{{ summary.totals[p.key].visitors }} 位訪客 · {{ summary.totals[p.key].views }} 次頁面瀏覽</p>
          </div>
        </div>

        <div class="visitors__row">
          <section class="panel panel--sources">
            <h3 class="panel__title">來源分布 <span class="panel__hint">近 30 天</span></h3>
            <p v-if="!summary.sources.length" class="panel__empty">還沒有資料</p>
            <table v-else class="v-table">
              <thead><tr><th>來源</th><th class="text-right">造訪</th><th class="text-right">占比</th></tr></thead>
              <tbody>
                <tr v-for="s in summary.sources" :key="s.source" class="v-row">
                  <td class="v-cell v-cell--strong">{{ s.source }}</td>
                  <td class="v-cell text-right">{{ s.sessions }}</td>
                  <td class="v-cell text-right">{{ pct(s.sessions) }}%</td>
                </tr>
              </tbody>
            </table>
          </section>

          <section class="panel panel--links">
            <h3 class="panel__title">追蹤連結</h3>
            <p class="panel__desc">LinkedIn App 和 104 常常不會告訴網站「從哪裡點進來」。貼在履歷或個人檔案上的網址改用下面的連結，來源就能準確分類。</p>
            <div v-for="l in trackingLinks" :key="l.src" class="link-row">
              <span class="link-row__label">{{ l.label }}</span>
              <code class="link-row__url">{{ linkFor(l.src) }}</code>
              <button class="link-row__btn" @click="copy(l.src)">{{ copied === l.src ? '已複製' : '複製' }}</button>
            </div>
          </section>
        </div>

        <section class="panel">
          <h3 class="panel__title">最近造訪 <span class="panel__hint">最近 {{ summary.recent.length }} 筆，時間為台灣時間</span></h3>
          <p v-if="!summary.recent.length" class="panel__empty">還沒有資料</p>
          <div v-else class="v-table-wrap">
            <table class="v-table">
              <thead>
                <tr><th>時間</th><th>來源</th><th>裝置</th><th>瀏覽器</th><th>看了哪些頁面</th><th class="text-right">停留</th></tr>
              </thead>
              <tbody>
                <tr v-for="s in summary.recent" :key="s.sessionId" class="v-row">
                  <td class="v-cell v-cell--nowrap">
                    {{ formatTime(s.startedAt) }}
                    <span v-if="s.returning" class="badge">回訪</span>
                  </td>
                  <td class="v-cell v-cell--strong v-cell--nowrap">{{ s.source }}</td>
                  <td class="v-cell v-cell--nowrap">{{ s.device }}</td>
                  <td class="v-cell v-cell--nowrap">{{ s.browser }}</td>
                  <td class="v-cell">{{ s.pages.map(pageLabel).join(' → ') }}</td>
                  <td class="v-cell v-cell--nowrap text-right">{{ duration(s) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getVisitSummary } from '@/api/visits'
import type { VisitSummary, VisitSession } from '@/types/visits'

const summary = ref<VisitSummary | null>(null)
const error = ref('')
const copied = ref('')

const periods = [
  { key: 'today', label: '今天' },
  { key: 'last7', label: '近 7 天' },
  { key: 'last30', label: '近 30 天' },
  { key: 'all', label: '全部' },
] as const

const trackingLinks = [
  { src: 'linkedin', label: 'LinkedIn' },
  { src: '104', label: '104' },
  { src: 'resume', label: '履歷 PDF' },
]

const PAGE_LABELS: Record<string, string> = {
  '/': '首頁', '/activities': '課外活動', '/social': '社會參與',
  '/literature': '文學天地', '/market': '市場消息', '/news': '總經新聞',
}

onMounted(async () => {
  try {
    summary.value = await getVisitSummary()
  } catch (e) {
    error.value = `讀取失敗：${(e as Error).message}`
  }
})

function pct(n: number): number {
  const total = summary.value?.sources.reduce((sum, s) => sum + s.sessions, 0) ?? 0
  return total ? Math.round((n / total) * 100) : 0
}

function pageLabel(path: string): string {
  return PAGE_LABELS[path] ?? path
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleString('zh-TW', {
    timeZone: 'Asia/Taipei', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false,
  })
}

function duration(s: VisitSession): string {
  const sec = Math.round((new Date(s.lastAt).getTime() - new Date(s.startedAt).getTime()) / 1000)
  if (sec < 1) return '—'
  if (sec < 60) return `${sec} 秒`
  return `${Math.floor(sec / 60)} 分 ${sec % 60} 秒`
}

function linkFor(src: string): string {
  return `${location.origin}/?src=${src}`
}

async function copy(src: string) {
  try {
    await navigator.clipboard.writeText(linkFor(src))
    copied.value = src
    setTimeout(() => { if (copied.value === src) copied.value = '' }, 1500)
  } catch { /* clipboard unavailable */ }
}
</script>

<style scoped>
.visitors { padding: var(--space-7) var(--space-6) var(--space-8); background: var(--color-white); }
.visitors__inner { max-width: var(--container-max); margin: 0 auto; display: flex; flex-direction: column; gap: var(--space-6); }
.visitors__error { font-family: var(--font-cjk); font-size: 14px; color: #dc2626; }

.metric-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); }
.metric-card { border: 1px solid var(--color-ink-4); border-top: 3px solid var(--color-primary); border-radius: var(--radius-md); padding: var(--space-4) var(--space-5); display: flex; flex-direction: column; gap: var(--space-1); }
.metric-card__label { font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-3); }
.metric-card__value { font-family: var(--font-body); font-size: 24px; font-weight: 700; color: var(--color-ink-1); }
.metric-card__unit { font-family: var(--font-cjk); font-size: 13px; font-weight: 400; color: var(--color-ink-3); }
.metric-card__sub { font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-3); }

.visitors__row { display: flex; gap: var(--space-6); }
.panel { display: flex; flex-direction: column; gap: var(--space-3); min-width: 0; }
.panel--sources { flex: 1; }
.panel--links { flex: 1.4; }
.panel__title { font-family: var(--font-cjk); font-size: 16px; font-weight: 700; color: var(--color-ink-1); }
.panel__hint { font-size: 12px; font-weight: 400; color: var(--color-ink-3); margin-left: var(--space-2); }
.panel__desc { font-family: var(--font-cjk); font-size: 13px; line-height: 1.6; color: var(--color-ink-2); }
.panel__empty { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-3); }

.link-row { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-2) 0; border-bottom: 1px solid var(--color-ink-4); }
.link-row__label { font-family: var(--font-cjk); font-size: 13px; font-weight: 700; color: var(--color-ink-1); width: 64px; flex-shrink: 0; }
.link-row__url { flex: 1; min-width: 0; font-family: var(--font-mono); font-size: 12px; color: var(--color-ink-2); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.link-row__btn { flex-shrink: 0; padding: 4px 12px; border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); background: var(--color-white); color: var(--color-ink-1); font-family: var(--font-cjk); font-size: 12px; cursor: pointer; }
.link-row__btn:hover { background: var(--color-primary-bg); border-color: var(--color-primary); }

.v-table-wrap { overflow-x: auto; }
.v-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.v-table th { padding: var(--space-2) var(--space-3); background: var(--color-primary-bg); font-family: var(--font-cjk); font-weight: 700; color: var(--color-ink-1); border-bottom: 2px solid var(--color-primary); text-align: left; white-space: nowrap; }
.v-row:nth-child(even) { background: #fafafa; }
.v-row:hover { background: var(--color-primary-bg); }
.v-cell { padding: var(--space-2) var(--space-3); font-family: var(--font-cjk); color: var(--color-ink-2); border-bottom: 1px solid var(--color-ink-4); }
.v-cell--strong { font-weight: 700; color: var(--color-ink-1); }
.v-cell--nowrap { white-space: nowrap; }
.v-table th.text-right, .text-right { text-align: right; }

.badge { display: inline-block; margin-left: var(--space-2); padding: 1px 6px; border-radius: var(--radius-sm); background: #eff6ff; color: #2563eb; font-size: 11px; font-weight: 700; }

@media (max-width: 900px) {
  .metric-cards { grid-template-columns: repeat(2, 1fr); }
  .visitors__row { flex-direction: column; }
}
@media (max-width: 640px) {
  .visitors { padding: var(--space-6) var(--space-4) var(--space-7); }
}
</style>
