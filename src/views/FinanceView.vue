<template>
  <div class="finance">
    <div class="finance__inner">

      <!-- Metric Cards -->
      <div v-if="summary" class="metric-cards">
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

      <!-- Charts + Holdings Table -->
      <div class="finance__body">

        <!-- Left: Donut Charts -->
        <div class="charts-col">
          <h3 class="charts-col__title">資產配置</h3>
          <div class="donut-wrap">
            <svg class="donut" viewBox="0 0 120 120">
              <circle class="donut__track" cx="60" cy="60" r="46" />
              <!-- TWD slice -->
              <circle
                class="donut__slice donut__slice--twd"
                cx="60" cy="60" r="46"
                :stroke-dasharray="`${twdArc} ${circumference - twdArc}`"
                stroke-dashoffset="0"
              />
              <!-- USD slice -->
              <circle
                class="donut__slice donut__slice--usd"
                cx="60" cy="60" r="46"
                :stroke-dasharray="`${usdArc} ${circumference - usdArc}`"
                :stroke-dashoffset="-(twdArc)"
              />
            </svg>
            <div class="donut-legend">
              <div class="donut-legend__item">
                <span class="donut-legend__dot donut-legend__dot--twd"></span>
                <span>TWD {{ twdPct }}%</span>
              </div>
              <div class="donut-legend__item">
                <span class="donut-legend__dot donut-legend__dot--usd"></span>
                <span>USD {{ usdPct }}%</span>
              </div>
            </div>
          </div>

          <h3 class="charts-col__title charts-col__title--mt">券商分布</h3>
          <div class="donut-wrap">
            <svg class="donut" viewBox="0 0 120 120">
              <circle class="donut__track" cx="60" cy="60" r="46" />
              <circle
                class="donut__slice donut__slice--broker1"
                cx="60" cy="60" r="46"
                :stroke-dasharray="`${broker1Arc} ${circumference - broker1Arc}`"
                stroke-dashoffset="0"
              />
              <circle
                class="donut__slice donut__slice--broker2"
                cx="60" cy="60" r="46"
                :stroke-dasharray="`${broker2Arc} ${circumference - broker2Arc}`"
                :stroke-dashoffset="-(broker1Arc)"
              />
            </svg>
            <div class="donut-legend">
              <div class="donut-legend__item">
                <span class="donut-legend__dot donut-legend__dot--broker1"></span>
                <span>國泰世華 {{ broker1Pct }}%</span>
              </div>
              <div class="donut-legend__item">
                <span class="donut-legend__dot donut-legend__dot--broker2"></span>
                <span>富邦 {{ broker2Pct }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Holdings Table -->
        <div class="holdings-col">
          <h3 class="holdings-col__title">持股明細</h3>
          <div class="holdings-table-wrap">
            <table class="holdings-table">
              <thead>
                <tr>
                  <th>股票代碼</th>
                  <th>名稱</th>
                  <th>幣別</th>
                  <th>券商</th>
                  <th class="text-right">股數</th>
                  <th class="text-right">均價</th>
                  <th class="text-right">市價</th>
                  <th class="text-right">市值</th>
                  <th class="text-right">損益</th>
                  <th class="text-right">報酬率</th>
                  <th class="text-right">累積股息</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="h in holdings" :key="h.id" class="holdings-row">
                  <td class="holdings-cell holdings-cell--symbol">{{ h.symbol }}</td>
                  <td class="holdings-cell">{{ h.name }}</td>
                  <td class="holdings-cell">
                    <span class="currency-badge" :class="`currency-badge--${h.currency.toLowerCase()}`">{{ h.currency }}</span>
                  </td>
                  <td class="holdings-cell">{{ h.broker }}</td>
                  <td class="holdings-cell text-right">{{ h.shares }}</td>
                  <td class="holdings-cell text-right">{{ h.avgPrice.toFixed(2) }}</td>
                  <td class="holdings-cell text-right">{{ h.marketPrice.toFixed(2) }}</td>
                  <td class="holdings-cell text-right">{{ h.currentValue.toLocaleString() }}</td>
                  <td class="holdings-cell text-right" :class="h.pnl >= 0 ? 'cell--up' : 'cell--down'">
                    {{ h.pnl >= 0 ? '+' : '' }}{{ h.pnl.toLocaleString() }}
                  </td>
                  <td class="holdings-cell text-right" :class="h.returnRate >= 0 ? 'cell--up' : 'cell--down'">
                    {{ h.returnRate >= 0 ? '+' : '' }}{{ h.returnRate.toFixed(2) }}%
                  </td>
                  <td class="holdings-cell text-right">{{ h.dividend || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getHoldings, getPortfolioSummary } from '@/api/finance'
import type { Holding, PortfolioSummary } from '@/types/finance'

const holdings = ref<Holding[]>([])
const summary = ref<PortfolioSummary | null>(null)

onMounted(async () => {
  holdings.value = await getHoldings()
  summary.value = await getPortfolioSummary()
})

// Donut chart math
const circumference = 2 * Math.PI * 46 // ≈ 289

const twdTotal = computed(() => holdings.value.filter((h) => h.currency === 'TWD').reduce((s, h) => s + h.currentValue, 0))
const usdTotal = computed(() => holdings.value.filter((h) => h.currency === 'USD').reduce((s, h) => s + h.currentValue, 0))
const grandTotal = computed(() => twdTotal.value + usdTotal.value)

const twdPct = computed(() => grandTotal.value ? Math.round((twdTotal.value / grandTotal.value) * 100) : 0)
const usdPct = computed(() => 100 - twdPct.value)
const twdArc = computed(() => (twdPct.value / 100) * circumference)
const usdArc = computed(() => (usdPct.value / 100) * circumference)

const guotaiTotal = computed(() => holdings.value.filter((h) => h.broker === '國泰世華').reduce((s, h) => s + h.currentValue, 0))
const fubonTotal  = computed(() => holdings.value.filter((h) => h.broker === '富邦').reduce((s, h) => s + h.currentValue, 0))
const broker1Pct = computed(() => grandTotal.value ? Math.round((guotaiTotal.value / grandTotal.value) * 100) : 0)
const broker2Pct = computed(() => 100 - broker1Pct.value)
const broker1Arc = computed(() => (broker1Pct.value / 100) * circumference)
const broker2Arc = computed(() => (broker2Pct.value / 100) * circumference)
</script>

<style scoped>
.finance {
  padding: var(--space-7) var(--space-6) var(--space-8);
  background: var(--color-white);
}

.finance__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-7);
}

/* ── Metric cards ── */
.metric-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--space-4);
}

.metric-card {
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.metric-card--twd     { border-top: 3px solid var(--color-primary); }
.metric-card--pnl     { border-top: 3px solid #16a34a; }
.metric-card--div     { border-top: 3px solid var(--color-secondary); }
.metric-card--usd     { border-top: 3px solid var(--color-tertiary); }
.metric-card--usd-pnl { border-top: 3px solid #2563eb; }

.metric-card__label {
  font-family: var(--font-cjk);
  font-size: 12px;
  color: var(--color-ink-3);
}

.metric-card__value {
  font-family: var(--font-body);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.metric-card__value--up   { color: #16a34a; }
.metric-card__value--down { color: #dc2626; }

.metric-card__sub {
  font-size: 12px;
  color: var(--color-ink-3);
}

/* ── Body layout ── */
.finance__body {
  display: flex;
  gap: var(--space-6);
  align-items: flex-start;
}

/* ── Charts col ── */
.charts-col {
  flex-shrink: 0;
  width: 220px;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.charts-col__title {
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.charts-col__title--mt { margin-top: var(--space-4); }

.donut-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.donut { width: 120px; height: 120px; transform: rotate(-90deg); }

.donut__track {
  fill: none;
  stroke: var(--color-ink-4);
  stroke-width: 16;
}

.donut__slice {
  fill: none;
  stroke-width: 16;
  stroke-linecap: butt;
  transition: stroke-dasharray 0.8s ease;
}

.donut__slice--twd    { stroke: var(--color-primary); }
.donut__slice--usd    { stroke: var(--color-tertiary); }
.donut__slice--broker1 { stroke: var(--color-secondary); }
.donut__slice--broker2 { stroke: #2563eb; }

.donut-legend {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  align-self: flex-start;
  padding-left: var(--space-2);
}

.donut-legend__item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 13px;
  color: var(--color-ink-2);
}

.donut-legend__dot {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  flex-shrink: 0;
}

.donut-legend__dot--twd     { background: var(--color-primary); }
.donut-legend__dot--usd     { background: var(--color-tertiary); }
.donut-legend__dot--broker1 { background: var(--color-secondary); }
.donut-legend__dot--broker2 { background: #2563eb; }

/* ── Holdings table ── */
.holdings-col { flex: 1; overflow: hidden; }

.holdings-col__title {
  font-family: var(--font-cjk);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-ink-1);
  margin-bottom: var(--space-4);
}

.holdings-table-wrap { overflow-x: auto; }

.holdings-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.holdings-table th {
  padding: var(--space-2) var(--space-3);
  background: var(--color-primary-bg);
  font-family: var(--font-cjk);
  font-weight: 700;
  color: var(--color-ink-1);
  border-bottom: 2px solid var(--color-primary);
  white-space: nowrap;
}

.holdings-row:nth-child(even) { background: #fafafa; }
.holdings-row:hover { background: var(--color-primary-bg); }

.holdings-cell {
  padding: var(--space-2) var(--space-3);
  font-family: var(--font-body);
  color: var(--color-ink-2);
  border-bottom: 1px solid var(--color-ink-4);
  white-space: nowrap;
}

.holdings-cell--symbol { font-weight: 700; color: var(--color-ink-1); }

.text-right { text-align: right; }

.cell--up   { color: #16a34a; font-weight: 700; }
.cell--down { color: #dc2626; font-weight: 700; }

.currency-badge {
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 700;
}

.currency-badge--twd { background: var(--color-primary-bg); color: var(--color-ink-1); }
.currency-badge--usd { background: #eff6ff; color: #2563eb; }

@media (max-width: 900px) {
  .metric-cards { grid-template-columns: repeat(2, 1fr); }
  .finance__body { flex-direction: column; }
  .charts-col { width: 100%; flex-direction: row; flex-wrap: wrap; }
}
</style>
