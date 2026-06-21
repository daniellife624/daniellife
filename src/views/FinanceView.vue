<template>
  <div class="finance">
    <div class="finance__inner">
      <MetricCards v-if="summary" :summary="summary" />

      <div class="finance__body">
        <div class="charts-col">
          <h3 class="charts-col__title">資產配置</h3>
          <DonutChart :slices="allocationSlices" />

          <h3 class="charts-col__title charts-col__title--mt">券商分布</h3>
          <DonutChart :slices="brokerSlices" />
        </div>

        <HoldingsTable :holdings="holdings" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getHoldings, getPortfolioSummary } from '@/api/finance'
import type { Holding, PortfolioSummary } from '@/types/finance'
import MetricCards from '@/components/finance/MetricCards.vue'
import DonutChart from '@/components/finance/DonutChart.vue'
import HoldingsTable from '@/components/finance/HoldingsTable.vue'

const holdings = ref<Holding[]>([])
const summary  = ref<PortfolioSummary | null>(null)

onMounted(async () => {
  holdings.value = await getHoldings()
  summary.value  = await getPortfolioSummary()
})

const twdTotal   = computed(() => holdings.value.filter((h) => h.currency === 'TWD').reduce((s, h) => s + h.currentValue, 0))
const usdTotal   = computed(() => holdings.value.filter((h) => h.currency === 'USD').reduce((s, h) => s + h.currentValue, 0))
const grandTotal = computed(() => twdTotal.value + usdTotal.value)

const twdPct = computed(() => grandTotal.value ? Math.round((twdTotal.value / grandTotal.value) * 100) : 0)
const usdPct = computed(() => 100 - twdPct.value)

const guotaiTotal = computed(() => holdings.value.filter((h) => h.broker === '國泰世華').reduce((s, h) => s + h.currentValue, 0))
const broker1Pct = computed(() => grandTotal.value ? Math.round((guotaiTotal.value / grandTotal.value) * 100) : 0)
const broker2Pct = computed(() => 100 - broker1Pct.value)

const allocationSlices = computed(() => [
  { label: 'TWD', pct: twdPct.value,   color: 'var(--color-primary)' },
  { label: 'USD', pct: usdPct.value,   color: 'var(--color-tertiary)' },
])

const brokerSlices = computed(() => [
  { label: '國泰世華', pct: broker1Pct.value, color: 'var(--color-secondary)' },
  { label: '富邦',     pct: broker2Pct.value, color: '#2563eb' },
])
</script>

<style scoped>
.finance { padding: var(--space-7) var(--space-6) var(--space-8); background: var(--color-white); }

.finance__inner { max-width: var(--container-max); margin: 0 auto; display: flex; flex-direction: column; gap: var(--space-7); }

.finance__body { display: flex; gap: var(--space-6); align-items: flex-start; }

.charts-col { flex-shrink: 0; width: 220px; display: flex; flex-direction: column; gap: var(--space-3); }
.charts-col__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); }
.charts-col__title--mt { margin-top: var(--space-4); }

@media (max-width: 900px) {
  .finance__body { flex-direction: column; }
  .charts-col { width: 100%; flex-direction: row; flex-wrap: wrap; }
}
</style>
