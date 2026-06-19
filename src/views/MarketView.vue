<template>
  <div class="market">
    <div class="market__inner">

      <!-- ── 股票市場 ── -->
      <section class="market__section">
        <h2 class="market__section-title">股票市場 Stock Market</h2>
        <div class="market__grid market__grid--2">
          <div class="market__chart-wrap">
            <p class="market__chart-label">台股</p>
            <div ref="taiexEl" class="market__chart market__chart--lg"></div>
          </div>
          <div class="market__chart-wrap">
            <p class="market__chart-label">美股</p>
            <div ref="usEl" class="market__chart market__chart--lg"></div>
          </div>
        </div>
      </section>

      <!-- ── 外匯市場 ── -->
      <section class="market__section">
        <h2 class="market__section-title">外匯市場 Forex</h2>
        <div class="market__grid market__grid--3">
          <div class="market__chart-wrap">
            <p class="market__chart-label">USDTWD</p>
            <div ref="usdtwdEl" class="market__chart market__chart--md"></div>
          </div>
          <div class="market__chart-wrap">
            <p class="market__chart-label">JPYTWD</p>
            <div ref="jpytwdEl" class="market__chart market__chart--md"></div>
          </div>
          <div class="market__chart-wrap">
            <p class="market__chart-label">EURTWD</p>
            <div ref="eurtwdEl" class="market__chart market__chart--md"></div>
          </div>
        </div>
      </section>

      <!-- ── 利率與殖利率 — FRED iframe ── -->
      <section class="market__section">
        <h2 class="market__section-title">利率與殖利率 Yield</h2>
        <p class="market__section-sub">資料來源：<a href="https://fred.stlouisfed.org/" target="_blank" rel="noopener">FRED · St. Louis Fed</a></p>
        <div class="market__grid market__grid--2">
          <div class="market__chart-wrap">
            <p class="market__chart-label">美國10年期公債殖利率</p>
            <div class="market__chart market__chart--md">
              <iframe
                src="https://fred.stlouisfed.org/graph/?id=DGS10&cosd=2010-01-01&fq=Daily&fam=avg&fgst=lin&fgsnd=2010-01-01&line_index=1&transformation=lin&nd=2010-01-01"
                width="100%" height="100%"
                frameborder="0" scrolling="no"
                title="US 10-Year Treasury Yield — FRED"
              ></iframe>
            </div>
          </div>
          <div class="market__chart-wrap">
            <p class="market__chart-label">Fed 基準利率（聯邦基金目標利率）</p>
            <div class="market__chart market__chart--md">
              <iframe
                src="https://fred.stlouisfed.org/graph/?id=FEDFUNDS&cosd=2010-01-01"
                width="100%" height="100%"
                frameborder="0" scrolling="no"
                title="Federal Funds Rate — FRED"
              ></iframe>
            </div>
          </div>
        </div>
      </section>

      <!-- ── 總經指標 — World Bank API + bar chart ── -->
      <section class="market__section">
        <h2 class="market__section-title">其他總經重要指標</h2>
        <p class="market__section-sub">資料來源：<a href="https://data.worldbank.org/" target="_blank" rel="noopener">World Bank Open Data</a></p>
        <div class="market__grid market__grid--2">

          <!-- GDP -->
          <div class="market__chart-wrap">
            <p class="market__chart-label">GDP 成長率（美國，年增率 %）</p>
            <div class="market__chart market__chart--lg wb-box">
              <div v-if="gdpLoading" class="wb-state">載入中…</div>
              <div v-else-if="gdpError"  class="wb-state wb-state--err">資料載入失敗</div>
              <div v-else class="wb-chart">
                <div class="wb-chart__bars">
                  <div v-for="item in gdpData" :key="item.year" class="wb-col">
                    <span class="wb-col__val">{{ item.value > 0 ? '+' : '' }}{{ item.value }}%</span>
                    <div class="wb-col__wrap">
                      <div
                        class="wb-col__bar"
                        :class="item.value >= 0 ? 'wb-col__bar--pos' : 'wb-col__bar--neg'"
                        :style="{ height: (Math.abs(item.value) / gdpMax * 100) + '%' }"
                      ></div>
                    </div>
                    <span class="wb-col__year">{{ item.year.slice(2) }}</span>
                  </div>
                </div>
                <p class="wb-chart__code">NY.GDP.MKTP.KD.ZG · 2015–2024</p>
              </div>
            </div>
          </div>

          <!-- CPI -->
          <div class="market__chart-wrap">
            <p class="market__chart-label">CPI 通膨率（美國，年增率 %）</p>
            <div class="market__chart market__chart--lg wb-box">
              <div v-if="cpiLoading" class="wb-state">載入中…</div>
              <div v-else-if="cpiError"  class="wb-state wb-state--err">資料載入失敗</div>
              <div v-else class="wb-chart">
                <div class="wb-chart__bars">
                  <div v-for="item in cpiData" :key="item.year" class="wb-col">
                    <span class="wb-col__val">{{ item.value > 0 ? '+' : '' }}{{ item.value }}%</span>
                    <div class="wb-col__wrap">
                      <div
                        class="wb-col__bar wb-col__bar--cpi"
                        :style="{ height: (Math.abs(item.value) / cpiMax * 100) + '%' }"
                      ></div>
                    </div>
                    <span class="wb-col__year">{{ item.year.slice(2) }}</span>
                  </div>
                </div>
                <p class="wb-chart__code">FP.CPI.TOTL.ZG · 2015–2024</p>
              </div>
            </div>
          </div>

        </div>
      </section>


    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'

/* ─── TradingView chart refs ─── */
const taiexEl  = ref<HTMLElement | null>(null)
const usEl     = ref<HTMLElement | null>(null)
const usdtwdEl = ref<HTMLElement | null>(null)
const jpytwdEl = ref<HTMLElement | null>(null)
const eurtwdEl = ref<HTMLElement | null>(null)

const TV = 'https://s3.tradingview.com/external-embedding/'

function injectWidget(el: HTMLElement, widget: string, cfg: object) {
  const s = document.createElement('script')
  s.type  = 'text/javascript'
  s.src   = TV + widget
  s.async = true
  s.innerHTML = JSON.stringify(cfg)
  el.appendChild(s)
}

// Advanced Chart requires a tradingview-widget-container__widget inner div,
// otherwise the widget falls back to default symbol (AAPL).
function injectAdvancedChart(el: HTMLElement, cfg: object) {
  el.classList.add('tradingview-widget-container')
  const inner = document.createElement('div')
  inner.className = 'tradingview-widget-container__widget'
  inner.style.cssText = 'height:100%;width:100%'
  el.appendChild(inner)
  const s = document.createElement('script')
  s.type  = 'text/javascript'
  s.src   = TV + 'embed-widget-advanced-chart.js'
  s.async = true
  s.innerHTML = JSON.stringify(cfg)
  el.appendChild(s)
}

const advChartCfg = (symbol: string, timezone = 'Asia/Taipei') => ({
  autosize: true, symbol, interval: 'D', timezone,
  theme: 'light', style: '1', locale: 'zh_TW',
  enable_publishing: false, withdateranges: true, range: '6M',
  hide_side_toolbar: false, allow_symbol_change: true, save_image: false,
})

const miniCfg = (symbol: string, color: string, range = '1M') => ({
  symbol, width: '100%', height: '100%', locale: 'zh_TW', dateRange: range,
  colorTheme: 'light',
  trendLineColor: color,
  underLineColor: color.replace('1)', '0.28)'),
  underLineBottomColor: color.replace('1)', '0)'),
  isTransparent: false, autosize: true, largeChartUrl: '',
})

/* ─── World Bank types ─── */
interface WBEntry { year: string; value: number }

const gdpData    = ref<WBEntry[]>([])
const gdpLoading = ref(true)
const gdpError   = ref(false)
const gdpMax     = computed(() => Math.max(...gdpData.value.map(d => Math.abs(d.value)), 1))

const cpiData    = ref<WBEntry[]>([])
const cpiLoading = ref(true)
const cpiError   = ref(false)
const cpiMax     = computed(() => Math.max(...cpiData.value.map(d => Math.abs(d.value)), 1))

async function fetchWB(indicator: string): Promise<WBEntry[]> {
  const url = `https://api.worldbank.org/v2/country/US/indicator/${indicator}?format=json&mrv=10&per_page=10`
  const res = await fetch(url)
  if (!res.ok) throw new Error(res.statusText)
  const raw: [unknown, Record<string, unknown>[]] = await res.json()
  return raw[1]
    .filter(d => d.value !== null)
    .map(d => ({ year: d.date as string, value: Number(Number(d.value).toFixed(2)) }))
    .reverse()
}

/* ─── Mount ─── */
onMounted(async () => {

  /* Stocks — Advanced Chart with proper container structure so symbol config is applied */
  if (taiexEl.value) injectAdvancedChart(taiexEl.value, advChartCfg('TWSE:TAIEX'))
  if (usEl.value)    injectAdvancedChart(usEl.value,    advChartCfg('SP:SPX', 'America/New_York'))

  /* Forex */
  const blue = 'rgba(41,98,255,1)'
  ;[
    { el: usdtwdEl, symbol: 'FX_IDC:USDTWD' },
    { el: jpytwdEl, symbol: 'FX_IDC:JPYTWD' },
    { el: eurtwdEl, symbol: 'FX_IDC:EURTWD' },
  ].forEach(({ el, symbol }) => {
    if (el.value) injectWidget(el.value, 'embed-widget-mini-symbol-overview.js', miniCfg(symbol, blue, '1M'))
  })

  /* World Bank GDP */
  try {
    gdpData.value = await fetchWB('NY.GDP.MKTP.KD.ZG')
  } catch {
    gdpError.value = true
  } finally {
    gdpLoading.value = false
  }

  /* World Bank CPI */
  try {
    cpiData.value = await fetchWB('FP.CPI.TOTL.ZG')
  } catch {
    cpiError.value = true
  } finally {
    cpiLoading.value = false
  }

})
</script>

<style scoped>
.market {
  background: var(--color-white);
  min-height: 100vh;
}

.market__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-9);
}

/* Section */
.market__section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.market__section-title {
  font-family: var(--font-cjk);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.market__section-sub {
  font-family: var(--font-cjk);
  font-size: 12px;
  color: var(--color-ink-3);
  margin-top: -8px;
}

.market__section-sub a { color: var(--color-secondary); text-decoration: none; }
.market__section-sub a:hover { text-decoration: underline; }
.market__section-sub code {
  font-family: var(--font-body);
  background: var(--color-ink-5, #f2f2f2);
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 11px;
}

/* Grid */
.market__grid { display: grid; gap: var(--space-5); }
.market__grid--2 { grid-template-columns: 1fr 1fr; }
.market__grid--3 { grid-template-columns: 1fr 1fr 1fr; }

.market__chart-wrap {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.market__chart-label {
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-ink-2);
  text-align: center;
}

.market__chart {
  width: 100%;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.market__chart--lg { height: 460px; }
.market__chart--md { height: 300px; }

/* ── World Bank bar chart ── */
.wb-box {
  display: flex;
  align-items: stretch;
  padding: var(--space-4);
  box-sizing: border-box;
}

.wb-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
}

.wb-state--err { color: #d44; }

.wb-chart {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.wb-chart__bars {
  flex: 1;
  display: flex;
  align-items: flex-end;
  gap: 6px;
}

.wb-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  height: 100%;
}

.wb-col__val {
  font-size: 10px;
  font-weight: 600;
  color: var(--color-ink-2);
  white-space: nowrap;
  line-height: 1;
}

.wb-col__wrap {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.wb-col__bar {
  width: 100%;
  border-radius: 3px 3px 0 0;
  transition: height 0.8s cubic-bezier(0.22, 0.61, 0.36, 1);
  min-height: 3px;
}

.wb-col__bar--pos { background: #2962ff; }
.wb-col__bar--neg { background: #dc3c3c; border-radius: 0 0 3px 3px; }
.wb-col__bar--cpi { background: var(--color-primary); }

.wb-col__year {
  font-size: 10px;
  color: var(--color-ink-3);
  line-height: 1;
}

.wb-chart__code {
  font-size: 10px;
  color: var(--color-ink-4);
  font-family: var(--font-body);
  text-align: right;
}

/* ── RWD ── */
@media (max-width: 900px) {
  .market__grid--3 { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 767px) {
  .market__grid--2,
  .market__grid--3 { grid-template-columns: 1fr; }
}
</style>
