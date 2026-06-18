<template>
  <div class="literature">

    <!-- Train Timeline (LED 面板風格) -->
    <section class="timeline-section">
      <div class="timeline-section__inner">
        <div class="timeline-section__track">
          <div class="timeline-section__train">🚂</div>
          <div class="timeline-section__cards" ref="scrollEl">
            <div
              v-for="(evt, i) in timeline"
              :key="evt.id"
              class="timeline-card"
              :class="{ 'timeline-card--active': activeIndex === i }"
              @click="activeIndex = i"
            >
              <p class="timeline-card__grade">{{ evt.gradeLabel }}</p>
              <p class="timeline-card__award">{{ evt.awardTitle }}</p>
              <p class="timeline-card__result">{{ evt.result }}</p>
              <div class="timeline-card__nav">
                <button @click.stop="activeIndex = Math.max(0, activeIndex - 1)">◄</button>
                <span>{{ evt.date }}</span>
                <button @click.stop="activeIndex = Math.min(timeline.length - 1, activeIndex + 1)">►</button>
              </div>
              <div class="timeline-card__progress">
                <span>出生</span>
                <div class="timeline-card__bar">
                  <div class="timeline-card__bar-fill" :style="{ width: ((i + 1) / timeline.length * 100) + '%' }"></div>
                </div>
                <span>現在</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 文學跑馬燈 -->
    <section class="marquee-section">
      <div class="marquee-section__inner">
        <div class="marquee-track">
          <span v-for="n in 3" :key="n" class="marquee-content">
            得獎紀錄 &nbsp;·&nbsp; 創作分享 &nbsp;·&nbsp; 文字之道 &nbsp;·&nbsp; 語文競賽 &nbsp;·&nbsp;
          </span>
        </div>
      </div>
    </section>

    <!-- 文學作品 -->
    <section class="works-section">
      <div class="works-section__inner">
        <h2 class="page-title">文學作品</h2>
        <div class="works-grid">
          <div v-for="work in works" :key="work.id" class="work-card">
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
import { ref, onMounted } from 'vue'
import { getTimelineEvents, getLiteratureWorks } from '@/api/literature'
import type { TimelineEvent, LiteratureWork } from '@/types/literature'

const timeline = ref<TimelineEvent[]>([])
const works = ref<LiteratureWork[]>([])
const activeIndex = ref(0)
const scrollEl = ref<HTMLElement | null>(null)

onMounted(async () => {
  timeline.value = await getTimelineEvents()
  works.value = await getLiteratureWorks()
})
</script>

<style scoped>
.literature { background: var(--color-white); }

/* ── Train Timeline ── */
.timeline-section {
  background: #0a0a0a;
  padding: var(--space-7) 0;
  overflow: hidden;
}

.timeline-section__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--space-6);
}

.timeline-section__track {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.timeline-section__train {
  font-size: 32px;
  flex-shrink: 0;
}

.timeline-section__cards {
  display: flex;
  gap: var(--space-3);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -ms-overflow-style: none;
  scrollbar-width: none;
  flex: 1;
}

.timeline-section__cards::-webkit-scrollbar { display: none; }

.timeline-card {
  flex: 0 0 200px;
  scroll-snap-align: start;
  border: 1px solid #333;
  border-radius: var(--radius-sm);
  padding: var(--space-4);
  background: #111;
  color: #00FF41;
  font-family: 'Courier New', monospace;
  cursor: pointer;
  transition: border-color 0.2s;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.timeline-card--active { border-color: #00FF41; }

.timeline-card__grade { font-size: 12px; color: #888; }
.timeline-card__award { font-size: 13px; font-weight: 700; line-height: 1.4; }
.timeline-card__result { font-size: 12px; }

.timeline-card__nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  margin-top: auto;
}

.timeline-card__nav button {
  background: none;
  border: none;
  color: #00FF41;
  cursor: pointer;
  font-family: inherit;
  font-size: 12px;
}

.timeline-card__progress {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 10px;
  color: #555;
}

.timeline-card__bar {
  flex: 1;
  height: 3px;
  background: #333;
  border-radius: 2px;
  overflow: hidden;
}

.timeline-card__bar-fill {
  height: 100%;
  background: #00FF41;
  border-radius: 2px;
  transition: width 0.5s;
}

/* ── Marquee ── */
.marquee-section {
  background: #303030;
  padding: var(--space-3) 0;
  overflow: hidden;
}

.marquee-section__inner { overflow: hidden; }

.marquee-track {
  display: flex;
  white-space: nowrap;
  animation: marquee 18s linear infinite;
}

.marquee-content {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-white);
  padding-right: var(--space-6);
}

@keyframes marquee {
  from { transform: translateX(0); }
  to   { transform: translateX(-33.333%); }
}

/* ── Works ── */
.works-section {
  padding: var(--space-8) var(--space-6);
}

.works-section__inner {
  max-width: var(--container-max);
  margin: 0 auto;
}

.page-title {
  font-family: var(--font-cjk);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-ink-1);
  margin-bottom: var(--space-5);
}

.works-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
}

.work-card {
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.work-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-ink-4);
}

.work-card__title {
  font-family: var(--font-cjk);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.work-card__read-btn {
  padding: var(--space-1) var(--space-3);
  background: var(--color-secondary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 12px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.work-card__read-btn:hover { opacity: 0.82; }

.work-card__row {
  display: flex;
  align-items: stretch;
  border-bottom: 1px solid var(--color-ink-4);
}

.work-card__row:last-child { border-bottom: none; }

.work-card__label {
  width: 120px;
  flex-shrink: 0;
  padding: var(--space-2) var(--space-4);
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
  display: flex;
  align-items: center;
}

.work-card__val {
  flex: 1;
  padding: var(--space-2) var(--space-4);
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.work-card__val--yellow { background: var(--color-primary-bg); color: var(--color-ink-1); }
.work-card__val--green  { background: #eef1ec; color: var(--color-ink-1); }

@media (max-width: 767px) {
  .works-grid { grid-template-columns: 1fr; }
  .timeline-card { flex: 0 0 160px; }
}
</style>
