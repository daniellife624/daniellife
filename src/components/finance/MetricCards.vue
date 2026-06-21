<template>
  <div class="metric-cards">
    <div class="metric-card metric-card--twd">
      <p class="metric-card__label">TWD 總市值</p>
      <p class="metric-card__value">NT$ {{ summary.twdValue.toLocaleString() }}</p>
      <p class="metric-card__sub">更新於 {{ summary.updatedAt }}</p>
    </div>
    <div class="metric-card metric-card--pnl">
      <p class="metric-card__label">TWD 損益</p>
      <p class="metric-card__value" :class="summary.twdPnl >= 0 ? 'metric-card__value--up' : 'metric-card__value--down'">
        {{ summary.twdPnl >= 0 ? '+' : '' }}NT$ {{ summary.twdPnl.toLocaleString() }}
      </p>
      <p class="metric-card__sub">{{ summary.twdReturnRate >= 0 ? '+' : '' }}{{ summary.twdReturnRate }}%</p>
    </div>
    <div class="metric-card metric-card--div">
      <p class="metric-card__label">TWD 累積股息</p>
      <p class="metric-card__value">NT$ {{ summary.twdDividend.toLocaleString() }}</p>
      <p class="metric-card__sub">&nbsp;</p>
    </div>
    <div class="metric-card metric-card--usd">
      <p class="metric-card__label">USD 總市值</p>
      <p class="metric-card__value">US$ {{ summary.usdValue.toFixed(2) }}</p>
      <p class="metric-card__sub">損益 {{ summary.usdPnl >= 0 ? '+' : '' }}{{ summary.usdPnl.toFixed(2) }}</p>
    </div>
    <div class="metric-card metric-card--usd-pnl">
      <p class="metric-card__label">USD 報酬率</p>
      <p class="metric-card__value" :class="summary.usdReturnRate >= 0 ? 'metric-card__value--up' : 'metric-card__value--down'">
        {{ summary.usdReturnRate >= 0 ? '+' : '' }}{{ summary.usdReturnRate }}%
      </p>
      <p class="metric-card__sub">&nbsp;</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PortfolioSummary } from '@/types/finance'
defineProps<{ summary: PortfolioSummary }>()
</script>

<style scoped>
.metric-cards { display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--space-4); }

.metric-card { border: 1px solid var(--color-ink-4); border-radius: var(--radius-md); padding: var(--space-4) var(--space-5); display: flex; flex-direction: column; gap: var(--space-1); }

.metric-card--twd     { border-top: 3px solid var(--color-primary); }
.metric-card--pnl     { border-top: 3px solid #16a34a; }
.metric-card--div     { border-top: 3px solid var(--color-secondary); }
.metric-card--usd     { border-top: 3px solid var(--color-tertiary); }
.metric-card--usd-pnl { border-top: 3px solid #2563eb; }

.metric-card__label { font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-3); }
.metric-card__value { font-family: var(--font-body); font-size: 20px; font-weight: 700; color: var(--color-ink-1); }
.metric-card__value--up   { color: #16a34a; }
.metric-card__value--down { color: #dc2626; }
.metric-card__sub { font-size: 12px; color: var(--color-ink-3); }

@media (max-width: 900px) { .metric-cards { grid-template-columns: repeat(2, 1fr); } }
</style>
