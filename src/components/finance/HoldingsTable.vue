<template>
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
</template>

<script setup lang="ts">
import type { Holding } from '@/types/finance'
defineProps<{ holdings: Holding[] }>()
</script>

<style scoped>
.holdings-col { flex: 1; overflow: hidden; }
.holdings-col__title { font-family: var(--font-cjk); font-size: 16px; font-weight: 700; color: var(--color-ink-1); margin-bottom: var(--space-4); }
.holdings-table-wrap { overflow-x: auto; }
.holdings-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.holdings-table th { padding: var(--space-2) var(--space-3); background: var(--color-primary-bg); font-family: var(--font-cjk); font-weight: 700; color: var(--color-ink-1); border-bottom: 2px solid var(--color-primary); white-space: nowrap; }
.holdings-row:nth-child(even) { background: #fafafa; }
.holdings-row:hover { background: var(--color-primary-bg); }
.holdings-cell { padding: var(--space-2) var(--space-3); font-family: var(--font-body); color: var(--color-ink-2); border-bottom: 1px solid var(--color-ink-4); white-space: nowrap; }
.holdings-cell--symbol { font-weight: 700; color: var(--color-ink-1); }
.text-right { text-align: right; }
.cell--up   { color: #16a34a; font-weight: 700; }
.cell--down { color: #dc2626; font-weight: 700; }
.currency-badge { padding: 2px 6px; border-radius: var(--radius-sm); font-size: 11px; font-weight: 700; }
.currency-badge--twd { background: var(--color-primary-bg); color: var(--color-ink-1); }
.currency-badge--usd { background: #eff6ff; color: #2563eb; }
</style>
