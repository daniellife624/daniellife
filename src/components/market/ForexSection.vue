<template>
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

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

const miniCfg = (symbol: string, color: string, range = '1M') => ({
  symbol, width: '100%', height: '100%', locale: 'zh_TW', dateRange: range,
  colorTheme: 'light', trendLineColor: color,
  underLineColor: color.replace('1)', '0.28)'),
  underLineBottomColor: color.replace('1)', '0)'),
  isTransparent: false, autosize: true, largeChartUrl: '',
})

onMounted(() => {
  const blue = 'rgba(41,98,255,1)'
  ;[
    { el: usdtwdEl, symbol: 'FX_IDC:USDTWD' },
    { el: jpytwdEl, symbol: 'FX_IDC:JPYTWD' },
    { el: eurtwdEl, symbol: 'FX_IDC:EURTWD' },
  ].forEach(({ el, symbol }) => {
    if (el.value) injectWidget(el.value, 'embed-widget-mini-symbol-overview.js', miniCfg(symbol, blue, '1M'))
  })
})
</script>

<style scoped>
.market__section { display: flex; flex-direction: column; gap: var(--space-4); }
.market__section-title { font-family: var(--font-cjk); font-size: 20px; font-weight: 700; color: var(--color-ink-1); }
.market__grid { display: grid; gap: var(--space-5); }
.market__grid--3 { grid-template-columns: 1fr 1fr 1fr; }
.market__chart-wrap { display: flex; flex-direction: column; gap: var(--space-2); }
.market__chart-label { font-family: var(--font-cjk); font-size: 14px; font-weight: 600; color: var(--color-ink-2); text-align: center; }
.market__chart { width: 100%; border: 1px solid var(--color-ink-4); border-radius: var(--radius-md); overflow: hidden; }
.market__chart--md { height: 300px; }

@media (max-width: 900px) { .market__grid--3 { grid-template-columns: 1fr 1fr; } }
@media (max-width: 767px) { .market__grid--3 { grid-template-columns: 1fr; } }
</style>
