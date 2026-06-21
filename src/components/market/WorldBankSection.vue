<template>
  <section class="market__section">
    <div class="market__section-head">
      <h2 class="market__section-title">其他總經重要指標</h2>
      <div class="wb-rtabs">
        <button class="wb-rtab" :class="{ 'wb-rtab--active': wbCountry === 'US' }" @click="switchWbCountry('US')">🇺🇸 美國</button>
        <button class="wb-rtab" :class="{ 'wb-rtab--active': wbCountry === 'TW' }" @click="switchWbCountry('TW')">🇹🇼 台灣</button>
      </div>
    </div>
    <p class="market__section-sub">資料來源：<a href="https://data.worldbank.org/" target="_blank" rel="noopener">World Bank Open Data</a></p>
    <div class="market__grid market__grid--2">

      <div class="market__chart-wrap">
        <p class="market__chart-label">GDP 成長率（{{ WB_LABEL[wbCountry] }}，年增率 %）</p>
        <div class="market__chart market__chart--lg wb-box">
          <div v-if="gdpLoading" class="wb-state">載入中…</div>
          <div v-else-if="gdpError" class="wb-state wb-state--err">資料載入失敗</div>
          <div v-else class="wb-chart">
            <div class="wb-chart__bars">
              <div v-for="item in gdpData" :key="item.year" class="wb-col">
                <span class="wb-col__val">{{ item.value > 0 ? '+' : '' }}{{ item.value }}%</span>
                <div class="wb-col__wrap">
                  <div class="wb-col__bar" :class="item.value >= 0 ? 'wb-col__bar--pos' : 'wb-col__bar--neg'" :style="{ height: (Math.abs(item.value) / gdpMax * 100) + '%' }"></div>
                </div>
                <span class="wb-col__year">{{ item.year.slice(2) }}</span>
              </div>
            </div>
            <p class="wb-chart__code">NY.GDP.MKTP.KD.ZG · 2015–2024</p>
          </div>
        </div>
      </div>

      <div class="market__chart-wrap">
        <p class="market__chart-label">CPI 通膨率（{{ WB_LABEL[wbCountry] }}，年增率 %）</p>
        <div class="market__chart market__chart--lg wb-box">
          <div v-if="cpiLoading" class="wb-state">載入中…</div>
          <div v-else-if="cpiError" class="wb-state wb-state--err">資料載入失敗</div>
          <div v-else class="wb-chart">
            <div class="wb-chart__bars">
              <div v-for="item in cpiData" :key="item.year" class="wb-col">
                <span class="wb-col__val">{{ item.value > 0 ? '+' : '' }}{{ item.value }}%</span>
                <div class="wb-col__wrap">
                  <div class="wb-col__bar wb-col__bar--cpi" :style="{ height: (Math.abs(item.value) / cpiMax * 100) + '%' }"></div>
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
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface WBEntry { year: string; value: number }

const wbCountry = ref<'US' | 'TW'>('US')
const WB_LABEL: Record<string, string> = { US: '美國', TW: '台灣' }

const gdpData    = ref<WBEntry[]>([])
const gdpLoading = ref(true)
const gdpError   = ref(false)
const gdpMax     = computed(() => Math.max(...gdpData.value.map(d => Math.abs(d.value)), 1))

const cpiData    = ref<WBEntry[]>([])
const cpiLoading = ref(true)
const cpiError   = ref(false)
const cpiMax     = computed(() => Math.max(...cpiData.value.map(d => Math.abs(d.value)), 1))

async function fetchWB(indicator: string, country = 'US'): Promise<WBEntry[]> {
  const url = `https://api.worldbank.org/v2/country/${country}/indicator/${indicator}?format=json&mrv=10&per_page=10`
  const res = await fetch(url)
  if (!res.ok) throw new Error(res.statusText)
  const raw: [unknown, Record<string, unknown>[]] = await res.json()
  return raw[1]
    .filter(d => d.value !== null)
    .map(d => ({ year: d.date as string, value: Number(Number(d.value).toFixed(2)) }))
    .reverse()
}

async function loadWbData() {
  gdpLoading.value = true; gdpError.value = false
  cpiLoading.value = true; cpiError.value = false
  const c = wbCountry.value
  try { gdpData.value = await fetchWB('NY.GDP.MKTP.KD.ZG', c) } catch { gdpError.value = true } finally { gdpLoading.value = false }
  try { cpiData.value = await fetchWB('FP.CPI.TOTL.ZG', c) } catch { cpiError.value = true } finally { cpiLoading.value = false }
}

function switchWbCountry(c: 'US' | 'TW') { wbCountry.value = c; loadWbData() }

onMounted(() => loadWbData())
</script>

<style scoped>
.market__section { display: flex; flex-direction: column; gap: var(--space-4); }
.market__section-head { display: flex; align-items: center; justify-content: space-between; gap: var(--space-4); }
.market__section-title { font-family: var(--font-cjk); font-size: 20px; font-weight: 700; color: var(--color-ink-1); }
.market__section-sub { font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-3); margin-top: -8px; }
.market__section-sub a { color: var(--color-secondary); text-decoration: none; }
.market__section-sub a:hover { text-decoration: underline; }

.wb-rtabs { display: flex; gap: 6px; }
.wb-rtab { padding: 4px 12px; border-radius: var(--radius-full); border: 1px solid var(--color-ink-4); background: transparent; font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-2); cursor: pointer; transition: background 0.15s, border-color 0.15s, color 0.15s; }
.wb-rtab--active { background: var(--color-primary); border-color: var(--color-primary); color: var(--color-ink-1); font-weight: 600; }
.wb-rtab:not(.wb-rtab--active):hover { border-color: var(--color-ink-3); color: var(--color-ink-1); }

.market__grid { display: grid; gap: var(--space-5); }
.market__grid--2 { grid-template-columns: 1fr 1fr; }
.market__chart-wrap { display: flex; flex-direction: column; gap: var(--space-2); }
.market__chart-label { font-family: var(--font-cjk); font-size: 14px; font-weight: 600; color: var(--color-ink-2); text-align: center; }
.market__chart { width: 100%; border: 1px solid var(--color-ink-4); border-radius: var(--radius-md); overflow: hidden; }
.market__chart--lg { height: 460px; }

.wb-box { display: flex; align-items: stretch; padding: var(--space-4); box-sizing: border-box; }
.wb-state { flex: 1; display: flex; align-items: center; justify-content: center; font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-3); }
.wb-state--err { color: #d44; }
.wb-chart { flex: 1; display: flex; flex-direction: column; gap: var(--space-3); }
.wb-chart__bars { flex: 1; display: flex; align-items: flex-end; gap: 6px; }
.wb-col { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; height: 100%; }
.wb-col__val { font-size: 10px; font-weight: 600; color: var(--color-ink-2); white-space: nowrap; line-height: 1; }
.wb-col__wrap { flex: 1; width: 100%; display: flex; flex-direction: column; justify-content: flex-end; }
.wb-col__bar { width: 100%; border-radius: 3px 3px 0 0; transition: height 0.8s cubic-bezier(0.22, 0.61, 0.36, 1); min-height: 3px; }
.wb-col__bar--pos { background: #2962ff; }
.wb-col__bar--neg { background: #dc3c3c; border-radius: 0 0 3px 3px; }
.wb-col__bar--cpi { background: var(--color-primary); }
.wb-col__year { font-size: 10px; color: var(--color-ink-3); line-height: 1; }
.wb-chart__code { font-size: 10px; color: var(--color-ink-4); font-family: var(--font-body); text-align: right; }

@media (max-width: 767px) { .market__grid--2 { grid-template-columns: 1fr; } }
</style>
