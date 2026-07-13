<template>
  <div class="mop">

    <div class="mop__header">
      <span class="mop__title">大盤行情</span>
      <div class="mop__tabs">
        <button
          v-for="tab in TABS"
          :key="tab.key"
          class="mop__tab"
          :class="{ 'mop__tab--active': activeTab === tab.key }"
          @click="switchTab(tab.key)"
        >{{ tab.label }}</button>
      </div>
    </div>

    <div v-if="dataUnavailable" class="mop__unavailable">
      <p class="mop__unavailable-text">目前無法取得即時報價，請稍後再試</p>
    </div>

    <div v-else class="mop__body">
      <div class="mop__list">
        <div
          v-for="(idx, i) in currentIndices"
          :key="idx.id"
          class="idx-row"
          :class="{
            'idx-row--active': selected === i,
            'idx-row--up':   idx.change > 0,
            'idx-row--down': idx.change < 0,
          }"
          @click="selected = i"
        >
          <div class="idx-row__meta">
            <span class="idx-row__name">{{ idx.name }}</span>
            <span v-if="idx.volume" class="idx-row__vol">{{ idx.volume }}</span>
          </div>
          <div v-if="idx.unavailable" class="idx-row__nums">
            <span class="idx-row__na">資料暫缺</span>
          </div>
          <div v-else class="idx-row__nums">
            <span class="idx-row__price">{{ fmtP(idx.price) }}</span>
            <span class="idx-row__chg">
              {{ idx.change >= 0 ? '▲' : '▼' }}&thinsp;{{ fmtN(Math.abs(idx.change)) }}
            </span>
          </div>
        </div>
      </div>

      <div class="mop__detail">
        <template v-if="ai.unavailable">
          <p class="mop__unavailable-text mop__unavailable-text--inline">此指數目前資料暫缺</p>
        </template>
        <template v-else>
          <p class="mop__feat-label">{{ ai.name }}</p>
          <p class="mop__feat-price" :class="ai.change >= 0 ? 'txt-up' : 'txt-down'">
            {{ fmtP(ai.price) }}
          </p>
          <p class="mop__feat-chg" :class="ai.change >= 0 ? 'txt-up' : 'txt-down'">
            {{ ai.change >= 0 ? '▲' : '▼' }}&thinsp;{{ fmtN(Math.abs(ai.change)) }}
            ({{ Math.abs(ai.changePct).toFixed(2) }}%)
          </p>
          <div class="mop__ohlc">
            <span>開盤&thinsp;<b>{{ fmtP(ai.open) }}</b></span>
            <span>最高&thinsp;<b>{{ fmtP(ai.high) }}</b></span>
            <span>最低&thinsp;<b>{{ fmtP(ai.low) }}</b></span>
            <span>昨收&thinsp;<b>{{ fmtP(ai.prev) }}</b></span>
          </div>

          <svg class="mop__spark" viewBox="0 0 200 70" preserveAspectRatio="none">
            <defs>
              <linearGradient :id="`sg-${uid}`" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%"   :stop-color="ai.change >= 0 ? '#16a34a' : '#dc2626'" stop-opacity="0.18"/>
                <stop offset="100%" :stop-color="ai.change >= 0 ? '#16a34a' : '#dc2626'" stop-opacity="0"/>
              </linearGradient>
            </defs>
            <polygon  :points="area(ai.intraday)" :fill="`url(#sg-${uid})`"/>
            <polyline :points="line(ai.intraday)" fill="none"
              :stroke="ai.change >= 0 ? '#16a34a' : '#dc2626'"
              stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/>
          </svg>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/api/client'

const props = defineProps<{ defaultTab?: 'TW' | 'ASIA' | 'EU' | 'US' }>()

const uid = Math.random().toString(36).slice(2, 7)

const TABS = [
  { key: 'TW',   label: '台股' },
  { key: 'ASIA', label: '亞股' },
  { key: 'EU',   label: '歐股' },
  { key: 'US',   label: '美股' },
] as const
type TabKey = (typeof TABS)[number]['key']

interface Entry {
  id: string; name: string
  price: number; change: number; changePct: number
  open: number; high: number; low: number; prev: number
  volume?: string; intraday: number[]
  unavailable?: boolean
}

interface QuoteRaw {
  price: number; change: number; changePct: number
  open: number; high: number; low: number; prev: number
}

const SYMBOL_NAMES: Record<TabKey, { sym: string; name: string; vol?: string }[]> = {
  TW: [
    { sym: '^TWII',   name: '加權指數', vol: '成交額' },
    { sym: '^TWO',    name: '上櫃指數' },
    { sym: 'TW_ELEC', name: '電子類' },
    { sym: 'TW_FIN',  name: '金融類' },
  ],
  ASIA: [
    { sym: '^N225',     name: '日經指數' },
    { sym: '^KS11',     name: '韓國綜合' },
    { sym: '^HSI',      name: '香港恒生' },
    { sym: '000001.SS', name: '上海綜合' },
  ],
  EU: [
    { sym: '^FTSE',     name: '英國富時' },
    { sym: '^GDAXI',    name: '德國DAX' },
    { sym: '^FCHI',     name: '法國CAC40' },
    { sym: '^STOXX50E', name: '歐洲50' },
  ],
  US: [
    { sym: '^GSPC', name: 'S&P 500' },
    { sym: '^DJI',  name: '道瓊工業' },
    { sym: '^IXIC', name: 'NASDAQ' },
    { sym: '^RUT',  name: '羅素2000' },
  ],
}

function genIntraday(price: number, chg: number, n = 48): number[] {
  const prev = price - chg
  const pts: number[] = []
  for (let i = 0; i <= n; i++) {
    const t = i / n
    const noise = Math.sin(i * 1.73) * price * 0.0007 + Math.cos(i * 3.14) * price * 0.0003
    pts.push(prev + chg * t + noise)
  }
  return pts
}

function unavailableEntry(sym: string, name: string, vol?: string): Entry {
  return {
    id: sym, name, price: 0, change: 0, changePct: 0,
    open: 0, high: 0, low: 0, prev: 0, volume: vol,
    intraday: [], unavailable: true,
  }
}

function fromRaw(sym: string, name: string, raw: Record<string, QuoteRaw>, vol?: string): Entry {
  const q = raw[sym]
  if (!q || q.price === 0) return unavailableEntry(sym, name, vol)
  return {
    id: sym, name,
    price: q.price, change: q.change, changePct: q.changePct,
    open: q.open || q.price,
    high: q.high || q.price,
    low:  q.low  || q.price,
    prev: q.prev || (q.price - q.change),
    volume: vol,
    intraday: genIntraday(q.price, q.change),
  }
}

const activeTab       = ref<TabKey>(props.defaultTab ?? 'TW')
const selected         = ref(0)
const dataUnavailable = ref(false)
const allData          = ref<Record<TabKey, Entry[]>>({ TW: [], ASIA: [], EU: [], US: [] })

const _FALLBACK: Entry = { id: '', name: '', price: 0, change: 0, changePct: 0, open: 0, high: 0, low: 0, prev: 0, intraday: [], unavailable: true }
const currentIndices = computed(() => allData.value[activeTab.value])
const ai = computed((): Entry => currentIndices.value[selected.value] ?? currentIndices.value[0] ?? _FALLBACK)

function switchTab(key: TabKey) { activeTab.value = key; selected.value = 0 }

function fmtP(n: number) { return n.toLocaleString('zh-TW', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }
function fmtN(n: number) { return n.toLocaleString('zh-TW', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }

function line(prices: number[]): string {
  if (prices.length < 2) return ''
  const lo = Math.min(...prices), hi = Math.max(...prices), rng = hi - lo || 1
  return prices.map((p, i) => {
    const x = (i / (prices.length - 1)) * 200
    const y = 64 - ((p - lo) / rng) * 60
    return `${x.toFixed(1)},${y.toFixed(1)}`
  }).join(' ')
}
function area(prices: number[]): string {
  if (prices.length < 2) return ''
  return `0,70 ${line(prices)} 200,70`
}

onMounted(async () => {
  try {
    const raw = await apiFetch<Record<string, QuoteRaw>>('/api/market/quotes')
    if (Object.keys(raw).length === 0) { dataUnavailable.value = true; return }

    const build = (key: TabKey): Entry[] =>
      SYMBOL_NAMES[key].map(({ sym, name, vol }) => fromRaw(sym, name, raw, vol))

    allData.value = { TW: build('TW'), ASIA: build('ASIA'), EU: build('EU'), US: build('US') }
  } catch {
    dataUnavailable.value = true
  }
})
</script>

<style scoped>
.mop {
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-white);
  display: flex;
  flex-direction: column;
}

.mop__header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-4);
  border-bottom: 1px solid var(--color-ink-4);
  background: #f8f8f7;
  flex-shrink: 0;
}

.mop__title {
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 700;
  color: var(--color-ink-1);
  white-space: nowrap;
}

.mop__tabs { display: flex; }

.mop__tab {
  padding: var(--space-1) var(--space-3);
  font-family: var(--font-cjk);
  font-size: 12px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  color: var(--color-ink-3);
  transition: color 0.12s, border-color 0.12s;
  white-space: nowrap;
}
.mop__tab:hover     { color: var(--color-ink-1); }
.mop__tab--active   { color: var(--color-ink-1); font-weight: 700; border-bottom-color: var(--color-primary); }

.mop__body {
  display: flex;
  flex: 1;
  min-height: 240px;
}

.mop__unavailable {
  flex: 1;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
}
.mop__unavailable-text {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
  text-align: center;
}
.mop__unavailable-text--inline { padding: var(--space-4) 0; }

.mop__list {
  width: 42%;
  flex-shrink: 0;
  border-right: 1px solid var(--color-ink-4);
  display: flex;
  flex-direction: column;
}

.idx-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-2) var(--space-3);
  cursor: pointer;
  border-bottom: 1px solid var(--color-ink-4);
  transition: background 0.1s;
  flex: 1;
}
.idx-row:last-child { border-bottom: none; }
.idx-row:hover,
.idx-row--active { background: var(--color-primary-bg); }

.idx-row__meta { display: flex; flex-direction: column; gap: 2px; }
.idx-row__name { font-family: var(--font-cjk); font-size: 13px; font-weight: 600; color: var(--color-ink-1); }
.idx-row__vol  { font-size: 10px; color: var(--color-ink-4); }

.idx-row__nums { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }
.idx-row__price { font-family: var(--font-body); font-size: 13px; font-weight: 700; color: var(--color-ink-1); }
.idx-row__chg   { font-family: var(--font-body); font-size: 11px; font-weight: 600; }
.idx-row__na    { font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-3); }
.idx-row--up   .idx-row__chg { color: #16a34a; }
.idx-row--down .idx-row__chg { color: #dc2626; }

.mop__detail {
  flex: 1;
  padding: var(--space-3) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: 3px;
  overflow: hidden;
}

.mop__feat-label { font-family: var(--font-cjk); font-size: 11px; color: var(--color-ink-3); }
.mop__feat-price { font-family: var(--font-body); font-size: 24px; font-weight: 700; line-height: 1.1; letter-spacing: -0.5px; }
.mop__feat-chg   { font-family: var(--font-body); font-size: 12px; font-weight: 600; }

.txt-up   { color: #16a34a; }
.txt-down { color: #dc2626; }

.mop__ohlc {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px var(--space-2);
  margin-top: var(--space-1);
  font-size: 11px;
  color: var(--color-ink-3);
  font-family: var(--font-body);
}
.mop__ohlc b { color: var(--color-ink-1); font-weight: 600; }

.mop__spark {
  flex: 1;
  width: 100%;
  min-height: 60px;
  margin-top: var(--space-1);
}
</style>
