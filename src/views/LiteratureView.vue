<template>
  <div class="literature">

    <!-- ── 水平鐵道時間軸 ── -->
    <section class="track-section" ref="sectionEl">
      <div class="track-section__inner">

        <div class="track-section__head">
          <h2 class="track-section__title">文學得獎紀錄</h2>
          <p class="track-section__sub">從出生到現在的文字旅程 · 點擊站牌查看作品</p>
        </div>

        <!-- 鐵道區域 -->
        <div class="track-container" ref="containerEl">

          <!-- 站牌卡片（在軌道上方） -->
          <div
            v-for="(evt, i) in timeline"
            :key="evt.id"
            class="station"
            :class="{ 'station--arrived': i < arrivedCount }"
            :style="{ left: stationPct(i) + '%' }"
            @click="evt.workId && scrollToWork(evt.workId)"
          >
            <!-- 站牌卡 -->
            <div class="station__card">
              <div class="station__card-top">
                <span class="station__grade">{{ evt.gradeLabel }}</span>
                <p class="station__award">{{ evt.awardTitle }}</p>
                <p class="station__result">{{ evt.result }}</p>
              </div>
              <div class="station__card-bottom">
                <div class="station__nav">
                  <button class="station__nav-btn" @click.stop="goStation(i - 1)">◄</button>
                  <span class="station__date">{{ evt.date }}</span>
                  <button class="station__nav-btn" @click.stop="goStation(i + 1)">►</button>
                </div>
                <div class="station__progress">
                  <span class="station__prog-lbl">出生</span>
                  <div class="station__bar">
                    <div class="station__bar-fill" :style="{ width: ((i + 1) / timeline.length * 100) + '%' }"></div>
                  </div>
                  <span class="station__prog-lbl">{{ evt.gradeLabel.split('／')[1]?.trim() || '現在' }}</span>
                </div>
              </div>
            </div>

            <!-- 連接柱 -->
            <div class="station__pole"></div>
            <!-- 軌道圓點 -->
            <div class="station__dot"></div>
          </div>

          <!-- 軌道底線 -->
          <div class="rail-bg"></div>
          <!-- 已走過的軌道（黃色填充） -->
          <div class="rail-fill" ref="railFillEl"></div>

          <!-- 🚂 火車 -->
          <div class="train-loco" ref="trainEl">🚂</div>

          <!-- 起點 / 終點標籤 -->
          <span class="rail-label rail-label--left">出生</span>
          <span class="rail-label rail-label--right">現在</span>
        </div>

      </div>
    </section>

    <!-- ── 文學作品 ── -->
    <section class="works-section" ref="worksSectionEl">
      <div class="works-inner">
        <h2 class="page-title">文學作品</h2>
        <div class="works-grid">
          <div v-for="work in works" :key="work.id" class="work-card" :data-work-id="work.id">
            <div class="work-card__header">
              <h3 class="work-card__title">{{ work.title }}</h3>
              <button class="work-card__read-btn">閱讀全文</button>
            </div>
            <div class="work-card__row">
              <span class="work-card__label">幾歲撰寫的作品</span>
              <span class="work-card__val work-card__val--yellow">{{ work.ageWritten }}歲</span>
            </div>
            <div class="work-card__row">
              <span class="work-card__label">撰寫期間</span>
              <span class="work-card__val work-card__val--yellow">{{ work.period }}</span>
            </div>
            <div class="work-card__row">
              <span class="work-card__label">得獎紀錄</span>
              <span class="work-card__val work-card__val--green">{{ work.awards }}</span>
            </div>
            <div class="work-card__row">
              <span class="work-card__label">摘要文字</span>
              <span class="work-card__val work-card__val--green">{{ work.summary }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { getTimelineEvents, getLiteratureWorks } from '@/api/literature'
import type { TimelineEvent, LiteratureWork } from '@/types/literature'

// ── Data ──
const timeline = ref<TimelineEvent[]>([])
const works    = ref<LiteratureWork[]>([])

// ── Refs ──
const sectionEl    = ref<HTMLElement | null>(null)
const containerEl  = ref<HTMLElement | null>(null)
const trainEl      = ref<HTMLElement | null>(null)
const railFillEl   = ref<HTMLElement | null>(null)
const worksSectionEl = ref<HTMLElement | null>(null)

// ── Animation state ──
const arrivedCount  = ref(0)
let animId: number | null = null
let animStart: number | null = null
let observer: IntersectionObserver | null = null

const RAIL_START = 8   // % from left
const RAIL_END   = 92  // % from left
const RAIL_RANGE = RAIL_END - RAIL_START
const DURATION   = 3800 // ms

// Station x-position as % of container
function stationPct(i: number): number {
  const n = timeline.value.length
  if (n <= 1) return (RAIL_START + RAIL_END) / 2
  return RAIL_START + (i / (n - 1)) * RAIL_RANGE
}

// Ease-in-out cubic
function easeInOut(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
}

function tick(ts: number) {
  if (animStart === null) animStart = ts
  const elapsed = ts - animStart
  const t       = Math.min(elapsed / DURATION, 1)
  const eased   = easeInOut(t)

  // Train position (% of container): starts just left of rail, ends at rail end
  const trainLeft = (RAIL_START - 3) + eased * (RAIL_RANGE + 5)
  if (trainEl.value)   trainEl.value.style.left = trainLeft + '%'

  // Rail fill: width from RAIL_START to train's current position
  const fillWidth = Math.max(0, trainLeft - RAIL_START)
  if (railFillEl.value) railFillEl.value.style.width = fillWidth + '%'

  // Reveal stations the train has passed
  const n = timeline.value.length
  let count = 0
  for (let i = 0; i < n; i++) {
    if (trainLeft >= stationPct(i) - 2) count++
    else break
  }
  if (count > arrivedCount.value) arrivedCount.value = count

  if (t < 1) {
    animId = requestAnimationFrame(tick)
  }
}

function resetTrainAnimation() {
  if (animId) cancelAnimationFrame(animId)
  animId = null
  animStart = null
  arrivedCount.value = 0
  if (trainEl.value)    trainEl.value.style.left    = (RAIL_START - 3) + '%'
  if (railFillEl.value) railFillEl.value.style.width = '0%'
}

function startAnimation() {
  resetTrainAnimation()
  animId = requestAnimationFrame(tick)
}

// Navigate to adjacent station
function goStation(idx: number) {
  const n = timeline.value.length
  if (idx < 0 || idx >= n) return
  const el = containerEl.value?.querySelectorAll('.station')[idx] as HTMLElement | undefined
  el?.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
}

// Scroll to work card
function scrollToWork(workId: number) {
  if (!worksSectionEl.value) return
  const el = worksSectionEl.value.querySelector(`[data-work-id="${workId}"]`) as HTMLElement | null
  const target = el ?? worksSectionEl.value
  target.scrollIntoView({ behavior: 'smooth', block: 'center' })
  if (el) {
    el.classList.add('work-card--highlight')
    setTimeout(() => el.classList.remove('work-card--highlight'), 1800)
  }
}

onMounted(async () => {
  timeline.value = await getTimelineEvents()
  works.value    = await getLiteratureWorks()

  // Trigger when section enters viewport; reset when leaving
  observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        startAnimation()
      } else {
        resetTrainAnimation()
      }
    },
    { threshold: 0.25 },
  )
  if (sectionEl.value) observer.observe(sectionEl.value)
})

onUnmounted(() => {
  if (animId) cancelAnimationFrame(animId)
  observer?.disconnect()
})
</script>

<style scoped>
.literature {
  background:
    radial-gradient(ellipse at 12% 38%, rgba(90, 45, 150, 0.38) 0%, transparent 52%),
    radial-gradient(ellipse at 88% 10%, rgba(25, 70, 155, 0.28) 0%, transparent 48%),
    radial-gradient(ellipse at 55% 85%, rgba(20, 55, 110, 0.22) 0%, transparent 50%),
    #0d0d1a;
}

/* ══════════════════════════════════════════
   鐵道區塊
══════════════════════════════════════════ */
.track-section {
  background: rgba(10, 8, 18, 0.72);
  padding: var(--space-7) 0 var(--space-8);
  overflow: hidden;
}

.track-section__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--space-6);
}

.track-section__head {
  margin-bottom: var(--space-7);
}

.track-section__title {
  font-family: var(--font-cjk);
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 6px;
}

.track-section__sub {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: #888;
}

/* ── 鐵道容器 ── */
.track-container {
  position: relative;
  height: 320px; /* total section height for this area */
}

/* ── 雙軌 + 枕木 ── */
/* Rail center at y = 241px (top 234 + height 14 / 2) */
.rail-bg {
  position: absolute;
  top: 234px;
  left: 8%;
  right: 8%;
  height: 14px;
  /* 枕木 (crossties) repeating pattern */
  background: repeating-linear-gradient(
    90deg,
    transparent 0px,
    transparent 14px,
    rgba(120, 90, 58, 0.55) 14px,
    rgba(120, 90, 58, 0.55) 26px
  );
  /* 上下雙軌 */
  border-top: 2.5px solid #505050;
  border-bottom: 2.5px solid #505050;
}

.rail-fill {
  position: absolute;
  top: 234px;
  left: 8%;
  height: 14px;
  width: 0;
  /* 已通過路段：黃色雙軌 + 淡黃填色 */
  border-top: 2.5px solid var(--color-primary);
  border-bottom: 2.5px solid var(--color-primary);
  background: rgba(232, 193, 58, 0.07);
  z-index: 2;
  pointer-events: none;
}

/* ── 🚂 火車 ── */
.train-loco {
  position: absolute;
  top: 241px;
  left: 5%; /* JS updates this */
  transform: scaleX(-1) translateY(-50%);
  font-size: 34px;
  line-height: 1;
  z-index: 5;
  pointer-events: none;
  filter: drop-shadow(0 0 6px rgba(232,193,58,0.4));
}

/* ── 起點 / 終點標籤 ── */
.rail-label {
  position: absolute;
  top: 253px;
  font-family: var(--font-cjk);
  font-size: 11px;
  color: #888;
  letter-spacing: 0.04em;
}

.rail-label--left  { left: 8%; }
.rail-label--right { right: 8%; }

/* ══════════════════════════════════════════
   站牌
══════════════════════════════════════════ */
/*
  Structure (top → bottom):
    .station__card  (card, ~155px tall)
    .station__pole  (1px × 30px connector)
    .station__dot   (12px circle on rail)

  Dot center must align with rail at y=240.
  cardHeight=155 + poleH=30 + dotRadius=6 = 191 → station top = 240-191 = 49px
*/
.station {
  position: absolute;
  top: 50px; /* dot center = 50+155+30+6 = 241px = rail center */
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: default;
}

/* ── Station card ── */
.station__card {
  width: 155px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 1px solid #383838;
  opacity: 0;
  transform: translateY(-14px);
  transition: opacity 0.45s ease, transform 0.45s ease, border-color 0.3s;
}

.station--arrived .station__card {
  opacity: 1;
  transform: translateY(0);
}

.station--arrived[style] {
  cursor: pointer;
}

/* Card top (dark content area) */
.station__card-top {
  background: rgba(38, 34, 48, 0.88);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  padding: var(--space-3) var(--space-3) var(--space-2);
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.station__grade {
  font-family: var(--font-cjk);
  font-size: 10px;
  color: #aaa;
  letter-spacing: 0.04em;
}

.station__award {
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  line-height: 1.4;
}

.station__result {
  font-family: var(--font-cjk);
  font-size: 12px;
  color: var(--color-primary);
}

/* Card bottom (darker area) */
.station__card-bottom {
  background: rgba(22, 20, 30, 0.9);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border-top: 1px solid #383838;
  padding: var(--space-2) var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.station__nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.station__nav-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 10px;
  cursor: pointer;
  padding: 0 2px;
  transition: color 0.2s;
}

.station__nav-btn:hover { color: var(--color-primary); }

.station__date {
  font-family: 'Courier New', monospace;
  font-size: 10px;
  color: #bbb;
}

.station__progress {
  display: flex;
  align-items: center;
  gap: 4px;
}

.station__prog-lbl {
  font-family: var(--font-cjk);
  font-size: 9px;
  color: #888;
  flex-shrink: 0;
  white-space: nowrap;
}

.station__bar {
  flex: 1;
  height: 3px;
  background: #3a3a3a;
  border-radius: 2px;
  overflow: hidden;
}

.station__bar-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 2px;
}

/* Pole connecting card to dot */
.station__pole {
  width: 1px;
  height: 30px;
  background: #484848;
  transition: background 0.4s;
}

.station--arrived .station__pole { background: #686868; }

/* Dot on the rail */
.station__dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #2e2e2e;
  border: 2px solid #555;
  transition: background 0.4s, border-color 0.4s;
  z-index: 3;
}

.station--arrived .station__dot {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

/* Hover: boost card border if has workId */
.station:has([data-work-id]):hover .station__card,
.station--arrived:hover .station__card {
  border-color: var(--color-primary);
}

/* ══════════════════════════════════════════
   文學作品  (台鐵月台時刻表風格)
══════════════════════════════════════════ */
.works-section {
  padding: var(--space-8) var(--space-6);
  background: rgba(8, 8, 16, 0.68);
}

.works-inner {
  max-width: var(--container-max);
  margin: 0 auto;
}

.page-title {
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 400;
  color: #aaa;
  margin-bottom: var(--space-5);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.works-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

/* ── 時刻板卡片 ── */
.work-card {
  background: rgba(22, 18, 38, 0.68);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 3px;
  overflow: hidden;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.work-card--highlight {
  border-color: #22c55e;
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.18);
}

/* 板頭：作品名稱 + 按鈕，左側黃條如月台編號 */
.work-card__header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 10px var(--space-4);
  background: rgba(35, 28, 60, 0.85);
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  border-left: 3px solid #e8c13a;
}

.work-card__title {
  flex: 1;
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 700;
  color: #e8c13a;
  letter-spacing: 0.04em;
  text-shadow: 0 0 10px rgba(232, 193, 58, 0.35);
}

/* 閱讀全文：LED 綠色邊框按鈕 */
.work-card__read-btn {
  padding: 3px 10px;
  background: transparent;
  color: #22c55e;
  border: 1px solid #22c55e;
  border-radius: 2px;
  font-family: 'Courier New', monospace;
  font-size: 11px;
  cursor: pointer;
  letter-spacing: 0.06em;
  transition: background 0.2s;
  text-shadow: 0 0 6px rgba(34, 197, 94, 0.45);
  white-space: nowrap;
}

.work-card__read-btn:hover { background: rgba(34, 197, 94, 0.1); }

/* 資料列 */
.work-card__row {
  display: flex;
  align-items: stretch;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.work-card__row:last-child { border-bottom: none; }

/* 欄位標籤（如時刻板欄位頭） */
.work-card__label {
  width: 108px;
  flex-shrink: 0;
  padding: 8px var(--space-3);
  font-family: var(--font-cjk);
  font-size: 11px;
  color: #aaa;
  display: flex;
  align-items: center;
  background: rgba(15, 12, 28, 0.7);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
}

/* 資料值（LED 顯示區） */
.work-card__val {
  flex: 1;
  padding: 8px var(--space-3);
  font-family: 'Courier New', monospace;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  background: rgba(10, 8, 20, 0.55);
  min-height: 36px;
  word-break: break-all;
}

/* 琥珀色 LED（年份/期間） */
.work-card__val--yellow {
  color: #e8c13a;
  text-shadow: 0 0 8px rgba(232, 193, 58, 0.5);
}

/* 綠色 LED（得獎/摘要） */
.work-card__val--green {
  color: #22c55e;
  text-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

/* ── RWD ── */
@media (max-width: 900px) {
  .track-container { overflow-x: auto; min-width: 760px; }
  .track-section { overflow-x: auto; }
}

@media (max-width: 767px) {
  .works-grid { grid-template-columns: 1fr; }
}
</style>
