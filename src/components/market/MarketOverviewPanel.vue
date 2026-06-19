<template>
  <div class="mop">

    <!-- ── Header ── -->
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

    <!-- ── Body: left list + right detail ── -->
    <div class="mop__body">

      <!-- Left: index rows -->
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
          <div class="idx-row__nums">
            <span class="idx-row__price">{{ fmtP(idx.price) }}</span>
            <span class="idx-row__chg">
              {{ idx.change >= 0 ? '▲' : '▼' }}&thinsp;{{ fmtN(Math.abs(idx.change)) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Right: featured detail + sparkline -->
      <div class="mop__detail">
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
      </div>

    </div>

    <p v-if="usingMock" class="mop__note">* 即時數據需後端串接，目前顯示示意資料</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

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
}

// Deterministic sparkline via sin/cos
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

function mk(id: string, name: string, price: number, chg: number, vol?: string): Entry {
  const prev = price - chg
  const pct  = (chg / prev) * 100
  const spd  = Math.abs(price * 0.004)
  return {
    id, name, price, change: chg, changePct: pct,
    open: prev + chg * 0.35,
    high: Math.max(prev + chg * 0.35, price) + spd * 0.15,
    low:  Math.min(prev + chg * 0.35, price) - spd * 0.15,
    prev, volume: vol,
    intraday: genIntraday(price, chg),
  }
}

const MOCK: Record<TabKey, Entry[]> = {
  TW: [
    mk('twii', '上市',  22839.45,  68.20, '成交 3,124億'),
    mk('two',  '上櫃',    256.78,   3.08, '成交 512億'),
    mk('elec', '電子',   1234.56,  -5.67, '成交 1,876億'),
    mk('fini', '金融',   2234.89,  45.60, '成交 383億'),
  ],
  ASIA: [
    mk('n225', '日經指數',  38947.21,  297.45),
    mk('ks11', '韓國綜合',   2648.36,   15.78),
    mk('hsi',  '香港恒生',  19234.56, -124.33),
    mk('ssec', '上海綜合',   3218.45,   12.67),
  ],
  EU: [
    mk('ftse',  '英國富時',   8312.45,   34.56),
    mk('dax',   '德國DAX',  18723.89,   87.34),
    mk('cac40', '法國CAC40',  7834.22,  -28.45),
    mk('stoxx', '歐洲50',     4923.78,   18.90),
  ],
  US: [
    mk('gspc', 'S&P 500',   5892.34,   24.56),
    mk('dji',  '道瓊工業', 43218.67,  178.45),
    mk('ixic', 'NASDAQ',   19234.56,   87.23),
    mk('rut',  '羅素2000',  2178.34,   -8.67),
  ],
}

const activeTab = ref<TabKey>(props.defaultTab ?? 'TW')
const selected  = ref(0)
const usingMock = ref(false)
const allData   = ref<Record<TabKey, Entry[]>>(JSON.parse(JSON.stringify(MOCK)))

const currentIndices = computed(() => allData.value[activeTab.value])
const ai = computed(() => currentIndices.value[selected.value] ?? currentIndices.value[0])

function switchTab(key: TabKey) { activeTab.value = key; selected.value = 0 }

// Formatting
function fmtP(n: number) { return n.toLocaleString('zh-TW', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }
function fmtN(n: number) { return n.toLocaleString('zh-TW', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }

// SVG sparkline math
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

// Try Yahoo Finance (browser-direct, might succeed)
onMounted(async () => {
  try {
    const syms = ['^TWII','^TWO','^N225','^KS11','^HSI','000001.SS','^FTSE','^GDAXI','^FCHI','^STOXX50E','^GSPC','^DJI','^IXIC','^RUT']
    const url  = `https://query2.finance.yahoo.com/v7/finance/quote?symbols=${syms.join(',')}`
    const res  = await fetch(url)
    if (!res.ok) throw new Error('yf')
    const json = await res.json()
    const results: Record<string, unknown>[] = json?.quoteResponse?.result ?? []
    if (!results.length) throw new Error('empty')

    const m: Record<string, Record<string, unknown>> = {}
    results.forEach(r => { m[r.symbol as string] = r })

    function fromYF(sym: string, name: string, vol?: string): Entry | null {
      const r = m[sym]
      if (!r) return null
      const price = r.regularMarketPrice as number ?? 0
      const chg   = r.regularMarketChange as number ?? 0
      const pct   = r.regularMarketChangePercent as number ?? 0
      return {
        id: sym, name, price, change: chg, changePct: pct,
        open: r.regularMarketOpen as number ?? price,
        high: r.regularMarketDayHigh as number ?? price,
        low:  r.regularMarketDayLow  as number ?? price,
        prev: r.regularMarketPreviousClose as number ?? (price - chg),
        volume: vol,
        intraday: genIntraday(price, chg),
      }
    }

    allData.value = {
      TW: [
        fromYF('^TWII', '上市', '成交額') ?? MOCK.TW[0],
        fromYF('^TWO',  '上櫃')           ?? MOCK.TW[1],
        MOCK.TW[2], MOCK.TW[3],
      ],
      ASIA: [
        fromYF('^N225',     '日經指數') ?? MOCK.ASIA[0],
        fromYF('^KS11',     '韓國綜合') ?? MOCK.ASIA[1],
        fromYF('^HSI',      '香港恒生') ?? MOCK.ASIA[2],
        fromYF('000001.SS', '上海綜合') ?? MOCK.ASIA[3],
      ],
      EU: [
        fromYF('^FTSE',     '英國富時')  ?? MOCK.EU[0],
        fromYF('^GDAXI',    '德國DAX')   ?? MOCK.EU[1],
        fromYF('^FCHI',     '法國CAC40') ?? MOCK.EU[2],
        fromYF('^STOXX50E', '歐洲50')    ?? MOCK.EU[3],
      ],
      US: [
        fromYF('^GSPC', 'S&P 500')   ?? MOCK.US[0],
        fromYF('^DJI',  '道瓊工業')  ?? MOCK.US[1],
        fromYF('^IXIC', 'NASDAQ')    ?? MOCK.US[2],
        fromYF('^RUT',  '羅素2000')  ?? MOCK.US[3],
      ],
    }
  } catch {
    usingMock.value = true
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

/* ── Header ── */
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
.mop__tab:hover          { color: var(--color-ink-1); }
.mop__tab--active        { color: var(--color-ink-1); font-weight: 700; border-bottom-color: var(--color-primary); }

/* ── Body ── */
.mop__body {
  display: flex;
  flex: 1;
  min-height: 240px;
}

/* Left list */
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
.idx-row--up   .idx-row__chg { color: #16a34a; }
.idx-row--down .idx-row__chg { color: #dc2626; }

/* Right detail */
.mop__detail {
  flex: 1;
  padding: var(--space-3) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: 3px;
  overflow: hidden;
}

.mop__feat-label {
  font-family: var(--font-cjk);
  font-size: 11px;
  color: var(--color-ink-3);
}
.mop__feat-price {
  font-family: var(--font-body);
  font-size: 24px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.5px;
}
.mop__feat-chg {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
}

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

/* Footer note */
.mop__note {
  font-size: 10px;
  color: var(--color-ink-4);
  padding: 2px var(--space-3) var(--space-2);
  font-family: var(--font-cjk);
  flex-shrink: 0;
}
</style>
