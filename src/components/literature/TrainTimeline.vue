<template>
  <section class="track-section" ref="sectionEl">
    <div class="track-section__inner">
      <div class="track-section__head">
        <h2 class="track-section__title">文學得獎紀錄</h2>
        <p class="track-section__sub">從出生到現在的文字旅程 · 點擊站牌查看作品</p>
      </div>

      <div class="track-container" ref="containerEl">
        <div
          v-for="(evt, i) in timeline"
          :key="evt.id"
          class="station"
          :class="{ 'station--arrived': i < arrivedCount }"
          :style="{ left: stationPct(i) + '%' }"
          @click="evt.workId && $emit('click-work', evt.workId)"
        >
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
          <div class="station__pole"></div>
          <div class="station__dot"></div>
        </div>

        <div class="rail-bg"></div>
        <div class="rail-fill" ref="railFillEl"></div>
        <div class="train-loco" ref="trainEl">🚂</div>
        <span class="rail-label rail-label--left">出生</span>
        <span class="rail-label rail-label--right">現在</span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { TimelineEvent } from '@/types/literature'

const props = defineProps<{ timeline: TimelineEvent[] }>()
defineEmits<{ 'click-work': [workId: number] }>()

const sectionEl   = ref<HTMLElement | null>(null)
const containerEl = ref<HTMLElement | null>(null)
const trainEl     = ref<HTMLElement | null>(null)
const railFillEl  = ref<HTMLElement | null>(null)

const arrivedCount = ref(0)
let animId: number | null = null
let animStart: number | null = null
let observer: IntersectionObserver | null = null

const RAIL_START = 8
const RAIL_END   = 92
const RAIL_RANGE = RAIL_END - RAIL_START
const DURATION   = 3800

function stationPct(i: number): number {
  const n = props.timeline.length
  if (n <= 1) return (RAIL_START + RAIL_END) / 2
  return RAIL_START + (i / (n - 1)) * RAIL_RANGE
}

function easeInOut(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
}

function tick(ts: number) {
  if (animStart === null) animStart = ts
  const elapsed = ts - animStart
  const t = Math.min(elapsed / DURATION, 1)
  const eased = easeInOut(t)

  const trainLeft = (RAIL_START - 3) + eased * (RAIL_RANGE + 5)
  if (trainEl.value) trainEl.value.style.left = trainLeft + '%'

  const fillWidth = Math.max(0, trainLeft - RAIL_START)
  if (railFillEl.value) railFillEl.value.style.width = fillWidth + '%'

  const n = props.timeline.length
  let count = 0
  for (let i = 0; i < n; i++) {
    if (trainLeft >= stationPct(i) - 2) count++
    else break
  }
  if (count > arrivedCount.value) arrivedCount.value = count

  if (t < 1) animId = requestAnimationFrame(tick)
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

function goStation(idx: number) {
  const n = props.timeline.length
  if (idx < 0 || idx >= n) return
  const el = containerEl.value?.querySelectorAll('.station')[idx] as HTMLElement | undefined
  el?.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
}

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      if (entries[0]?.isIntersecting) startAnimation()
      else resetTrainAnimation()
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
.track-section {
  background: #f5f2ee;
  padding: var(--space-7) 0 var(--space-8);
  overflow: hidden;
}

.track-section__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--space-6);
}

.track-section__head { margin-bottom: var(--space-7); }

.track-section__title {
  font-family: var(--font-cjk);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-ink-1);
  margin-bottom: 6px;
}

.track-section__sub { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-3); }

.track-container { position: relative; height: 320px; }

.rail-bg {
  position: absolute;
  top: 234px; left: 8%; right: 8%; height: 14px;
  background: repeating-linear-gradient(
    90deg, transparent 0px, transparent 14px,
    rgba(120, 90, 58, 0.45) 14px, rgba(120, 90, 58, 0.45) 26px
  );
  border-top: 2.5px solid #8a8a8a;
  border-bottom: 2.5px solid #8a8a8a;
}

.rail-fill {
  position: absolute;
  top: 234px; left: 8%; height: 14px; width: 0;
  border-top: 2.5px solid var(--color-primary);
  border-bottom: 2.5px solid var(--color-primary);
  background: rgba(232, 193, 58, 0.07);
  z-index: 2; pointer-events: none;
}

.train-loco {
  position: absolute;
  top: 241px; left: 5%;
  transform: scaleX(-1) translateY(-50%);
  font-size: 34px; line-height: 1; z-index: 5; pointer-events: none;
  filter: drop-shadow(0 0 6px rgba(232,193,58,0.4));
}

.rail-label {
  position: absolute; top: 253px;
  font-family: var(--font-cjk); font-size: 11px; color: var(--color-ink-3); letter-spacing: 0.04em;
}
.rail-label--left  { left: 8%; }
.rail-label--right { right: 8%; }

.station {
  position: absolute; top: 50px;
  transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; cursor: default;
}

.station__card {
  width: 155px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 1px solid #d8cfc4;
  opacity: 0; transform: translateY(-14px);
  transition: opacity 0.45s ease, transform 0.45s ease, border-color 0.3s;
}
.station--arrived .station__card { opacity: 1; transform: translateY(0); }
.station--arrived[style] { cursor: pointer; }

.station__card-top {
  background: #fffbf4;
  padding: var(--space-3) var(--space-3) var(--space-2);
  display: flex; flex-direction: column; gap: 3px;
}

.station__grade { font-family: var(--font-cjk); font-size: 10px; color: var(--color-ink-3); letter-spacing: 0.04em; }
.station__award { font-family: var(--font-cjk); font-size: 13px; font-weight: 700; color: var(--color-ink-1); line-height: 1.4; }
.station__result { font-family: var(--font-cjk); font-size: 12px; color: #8b6200; }

.station__card-bottom {
  background: #f0ebe2;
  border-top: 1px solid #d8cfc4;
  padding: var(--space-2) var(--space-3);
  display: flex; flex-direction: column; gap: var(--space-2);
}

.station__nav { display: flex; align-items: center; justify-content: space-between; }
.station__nav-btn { background: none; border: none; color: var(--color-ink-3); font-size: 10px; cursor: pointer; padding: 0 2px; transition: color 0.2s; }
.station__nav-btn:hover { color: var(--color-primary); }
.station__date { font-family: 'Courier New', monospace; font-size: 10px; color: #777; }

.station__progress { display: flex; align-items: center; gap: 4px; }
.station__prog-lbl { font-family: var(--font-cjk); font-size: 9px; color: var(--color-ink-3); flex-shrink: 0; white-space: nowrap; }
.station__bar { flex: 1; height: 3px; background: #d8cfc4; border-radius: 2px; overflow: hidden; }
.station__bar-fill { height: 100%; background: var(--color-primary); border-radius: 2px; }

.station__pole { width: 1px; height: 30px; background: #c4b8a8; transition: background 0.4s; }
.station--arrived .station__pole { background: #a89880; }

.station__dot { width: 12px; height: 12px; border-radius: 50%; background: #e0d8cc; border: 2px solid #b8a88a; transition: background 0.4s, border-color 0.4s; z-index: 3; }
.station--arrived .station__dot { background: var(--color-primary); border-color: var(--color-primary); }

.station--arrived:hover .station__card { border-color: var(--color-primary); }

@media (max-width: 900px) { .track-container { overflow-x: auto; min-width: 760px; } }
</style>
