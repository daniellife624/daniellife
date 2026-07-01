<template>
  <div class="mop">
    <div ref="widgetEl" class="mop__widget"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps<{ defaultTab?: 'TW' | 'ASIA' | 'EU' | 'US' }>()

const widgetEl = ref<HTMLElement | null>(null)

const TV = 'https://s3.tradingview.com/external-embedding/'

const ALL_TABS = {
  TW: {
    title: '台股',
    symbols: [
      { s: 'TWSE:TAIEX', d: '加權指數' },
      { s: 'INDEX:TWOTC', d: '上櫃指數' },
      { s: 'TWSE:ELEC', d: '電子類' },
      { s: 'TWSE:FINI', d: '金融類' },
    ],
  },
  ASIA: {
    title: '亞股',
    symbols: [
      { s: 'INDEX:NKY',    d: '日經225' },
      { s: 'INDEX:KOSPI',  d: '韓國KOSPI' },
      { s: 'INDEX:HSI',    d: '恒生指數' },
      { s: 'INDEX:SHCOMP', d: '上海綜合' },
    ],
  },
  EU: {
    title: '歐股',
    symbols: [
      { s: 'INDEX:UKX',    d: '英國富時100' },
      { s: 'INDEX:DAX',    d: '德國DAX' },
      { s: 'INDEX:CAC40',  d: '法國CAC40' },
      { s: 'INDEX:STOX5E', d: '歐洲50' },
    ],
  },
  US: {
    title: '美股',
    symbols: [
      { s: 'SP:SPX',      d: 'S&P 500' },
      { s: 'DJ:DJI',      d: '道瓊工業' },
      { s: 'NASDAQ:IXIC', d: 'NASDAQ' },
      { s: 'INDEX:RTY',   d: '羅素2000' },
    ],
  },
} as const

type TabKey = keyof typeof ALL_TABS

onMounted(() => {
  if (!widgetEl.value) return

  const first: TabKey = props.defaultTab ?? 'TW'
  const order: TabKey[] = [first, ...((['TW', 'ASIA', 'EU', 'US'] as TabKey[]).filter(t => t !== first))]
  const tabs = order.map(k => ALL_TABS[k])

  const config = {
    colorTheme: 'light',
    dateRange: '1D',
    showChart: true,
    locale: 'zh_TW',
    isTransparent: false,
    showSymbolLogo: false,
    showFloatingTooltip: false,
    width: '100%',
    height: '490',
    tabs,
  }

  const s = document.createElement('script')
  s.type = 'text/javascript'
  s.src = TV + 'embed-widget-market-overview.js'
  s.async = true
  s.innerHTML = JSON.stringify(config)
  widgetEl.value.appendChild(s)
})
</script>

<style scoped>
.mop {
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-white);
  height: 490px;
}

.mop__widget {
  width: 100%;
  height: 100%;
}
</style>
