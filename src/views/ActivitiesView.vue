<template>
  <div class="activities">

    <!-- 領導經驗 -->
    <section class="exp-section">
      <div class="exp-section__inner">
        <h2 class="page-title">領導經驗</h2>
        <div class="exp-list">
          <div
            v-for="item in leadershipItems"
            :key="item.id"
            class="exp-card"
          >
            <div class="exp-card__left">
              <h3 class="exp-card__title">{{ item.title }}</h3>
              <p class="exp-card__info">服務機構：{{ item.organization }}</p>
              <p class="exp-card__info">服務期間：{{ item.period }}</p>
              <p class="exp-card__contrib">主要貢獻：{{ item.contribution }}</p>
            </div>
            <div class="exp-card__right">
              <div class="exp-card__photos">
                <div class="exp-card__photo"></div>
                <div class="exp-card__photo"></div>
              </div>
              <button class="exp-card__btn" @click="openModal(item)">查看更多</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 社團經驗 -->
    <section class="exp-section exp-section--alt">
      <div class="exp-section__inner">
        <h2 class="page-title">社團經驗</h2>
        <div class="exp-list">
          <div
            v-for="item in clubItems"
            :key="item.id"
            class="exp-card"
          >
            <div class="exp-card__left">
              <h3 class="exp-card__title">{{ item.title }}</h3>
              <p class="exp-card__info">服務機構：{{ item.organization }}</p>
              <p class="exp-card__info">服務期間：{{ item.period }}</p>
              <p class="exp-card__contrib">主要貢獻：{{ item.contribution }}</p>
            </div>
            <div class="exp-card__right">
              <div class="exp-card__photos">
                <div class="exp-card__photo"></div>
                <div class="exp-card__photo"></div>
              </div>
              <button class="exp-card__btn" @click="openModal(item)">查看更多</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 造訪過國家 -->
    <section class="travel">
      <div class="travel__inner">
        <h2 class="page-title">造訪過國家</h2>
        <p class="travel__subtitle">丹尼的旅行日記 / 讓知識不再僅限於課本</p>
        <div class="travel__body">
          <!-- 圓形地圖佔位 -->
          <div class="travel__map">
            <div class="travel__map-placeholder">🗺</div>
          </div>
          <!-- 洲別列表 -->
          <div class="travel__continents">
            <div
              v-for="cont in continents"
              :key="cont.key"
              class="continent-card"
              :class="`continent-card--${cont.key.toLowerCase()}`"
            >
              <h4 class="continent-card__title">{{ cont.label }}</h4>
              <ul class="continent-card__list">
                <li v-if="!cont.entries.length" class="continent-card__empty">都還沒去過</li>
                <li
                  v-for="e in cont.entries"
                  :key="e.id"
                  class="continent-card__entry continent-card__entry--clickable"
                  @click="activeTravelEntry = e"
                >
                  <span class="continent-card__pin">📍</span>{{ e.country }}
                </li>
              </ul>
              <button class="continent-card__btn" :class="`continent-card__btn--${cont.key.toLowerCase()}`">
                新增國家、見聞
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Experience Modal -->
    <Teleport to="body">
      <div v-if="activeModal" class="modal-backdrop" @click.self="closeModal">
        <div class="modal">
          <button class="modal__close" @click="closeModal">×</button>
          <h3 class="modal__title">{{ activeModal.title }}</h3>
          <p class="modal__info">服務機構：{{ activeModal.organization }}</p>
          <p class="modal__info">服務期間：{{ activeModal.period }}</p>
          <div class="modal__photos">
            <div class="modal__photo"></div>
            <div class="modal__photo"></div>
          </div>
          <p class="modal__contrib">{{ activeModal.contribution }}</p>
        </div>
      </div>
    </Teleport>

    <!-- Travel Entry Modal -->
    <Teleport to="body">
      <div v-if="activeTravelEntry" class="modal-backdrop" @click.self="activeTravelEntry = null">
        <div class="modal travel-modal">
          <button class="modal__close" @click="activeTravelEntry = null">×</button>
          <div class="travel-modal__header">
            <span class="travel-modal__pin">📍</span>
            <h3 class="modal__title">{{ activeTravelEntry.country }}</h3>
          </div>
          <div class="travel-modal__meta-row">
            <span class="travel-modal__meta-item">城市：{{ activeTravelEntry.city }}</span>
            <span class="travel-modal__meta-item">洲別：{{ activeTravelEntry.continent }}</span>
            <span class="travel-modal__meta-item">造訪：{{ activeTravelEntry.visitedAt }}</span>
          </div>
          <div class="modal__photos">
            <div class="modal__photo"></div>
            <div class="modal__photo"></div>
          </div>
          <template v-if="activeTravelEntry.journal || activeTravelEntry.companions || activeTravelEntry.activities || activeTravelEntry.purchases">
            <div v-if="activeTravelEntry.companions" class="travel-modal__field">
              <span class="travel-modal__field-label">旅伴</span>
              <span class="travel-modal__field-value">{{ activeTravelEntry.companions }}</span>
            </div>
            <div v-if="activeTravelEntry.activities" class="travel-modal__field">
              <span class="travel-modal__field-label">主要活動</span>
              <span class="travel-modal__field-value">{{ activeTravelEntry.activities }}</span>
            </div>
            <div v-if="activeTravelEntry.purchases" class="travel-modal__field">
              <span class="travel-modal__field-label">購物清單</span>
              <span class="travel-modal__field-value">{{ activeTravelEntry.purchases }}</span>
            </div>
            <div v-if="activeTravelEntry.journal" class="travel-modal__journal">
              <p class="travel-modal__field-label">旅行日記</p>
              <p class="travel-modal__journal-text">{{ activeTravelEntry.journal }}</p>
            </div>
          </template>
          <p v-else class="travel-modal__empty">尚未填寫旅行見聞，可至後台新增。</p>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getExperiences, getTravelEntries, groupByContinent } from '@/api/activities'
import type { Experience, TravelEntry } from '@/types/activities'

const experiences = ref<Experience[]>([])
const activeModal = ref<Experience | null>(null)
const activeTravelEntry = ref<TravelEntry | null>(null)

const leadershipItems = computed(() => experiences.value.filter((e) => e.type === 'leadership'))
const clubItems = computed(() => experiences.value.filter((e) => e.type === 'club'))

const continents = ref(groupByContinent([]))

onMounted(async () => {
  experiences.value = await getExperiences()
  const entries = await getTravelEntries()
  continents.value = groupByContinent(entries)
})

function openModal(item: Experience) {
  activeModal.value = item
}

function closeModal() {
  activeModal.value = null
}
</script>

<style scoped>
.activities {
  background-color: var(--color-white);
}

/* 區塊 */
.exp-section {
  padding: var(--space-8) var(--space-6);
}

.exp-section--alt {
  background-color: #fafafa;
  border-top: 1px solid var(--color-ink-4);
}

.exp-section__inner {
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

/* 經歷卡片 */
.exp-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.exp-card {
  display: flex;
  gap: var(--space-5);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  background: var(--color-white);
}

.exp-card__left {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.exp-card__title {
  font-family: var(--font-cjk);
  font-size: 17px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.exp-card__info {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}

.exp-card__contrib {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.exp-card__right {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  width: 260px;
}

.exp-card__photos {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2);
}

.exp-card__photo {
  height: 100px;
  background-color: #f5efea;
  border-radius: var(--radius-sm);
}

.exp-card__btn {
  width: 100%;
  padding: var(--space-3) 0;
  background-color: var(--color-primary);
  color: var(--color-ink-1);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.exp-card__btn:hover { opacity: 0.82; }

/* 造訪過國家 */
.travel {
  padding: var(--space-8) var(--space-6);
  border-top: 1px solid var(--color-ink-4);
}

.travel__inner {
  max-width: var(--container-max);
  margin: 0 auto;
}

.travel__subtitle {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-3);
  margin-bottom: var(--space-6);
}

.travel__body {
  display: flex;
  gap: var(--space-6);
  align-items: flex-start;
}

.travel__map {
  flex-shrink: 0;
  width: 360px;
  height: 360px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid var(--color-ink-4);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e8f0f8;
}

.travel__map-placeholder {
  font-size: 80px;
}

.travel__continents {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  flex: 1;
}

/* 洲別卡片 */
.continent-card {
  border-radius: var(--radius-md);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  border: 1px solid var(--color-ink-4);
}

.continent-card__title {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 700;
}

.continent-card--europe   .continent-card__title { color: #2563eb; }
.continent-card--asia     .continent-card__title { color: var(--color-primary); }
.continent-card--africa   .continent-card__title { color: var(--color-ink-1); }
.continent-card--australia .continent-card__title { color: #0d9488; }
.continent-card--americas  .continent-card__title { color: var(--color-tertiary); }

.continent-card__list { list-style: none; flex: 1; }

.continent-card__empty {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
}

.continent-card__entry {
  display: flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}

.continent-card__pin { font-size: 12px; }

.continent-card__entry--clickable {
  cursor: pointer;
  border-radius: var(--radius-sm);
  padding: 2px 4px;
  margin: 0 -4px;
  transition: background 0.15s;
}
.continent-card__entry--clickable:hover { background: var(--color-primary-bg); }

.continent-card__btn {
  margin-top: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-full);
  border: none;
  font-family: var(--font-cjk);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.continent-card__btn:hover { opacity: 0.82; }

.continent-card--europe   .continent-card__btn { background: #2563eb; color: #fff; }
.continent-card--asia     .continent-card__btn { background: var(--color-primary); color: var(--color-ink-1); }
.continent-card--africa   .continent-card__btn { background: var(--color-ink-1); color: #fff; }
.continent-card--australia .continent-card__btn { background: #0d9488; color: #fff; }
.continent-card--americas  .continent-card__btn { background: var(--color-tertiary); color: #fff; }

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--color-white);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  width: 540px;
  max-width: 90vw;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.modal__close {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  font-size: 20px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-ink-3);
}

.modal__title {
  font-family: var(--font-cjk);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.modal__info {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}

.modal__photos {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
  margin: var(--space-2) 0;
}

.modal__photo {
  height: 140px;
  background-color: #f5efea;
  border-radius: var(--radius-sm);
}

.modal__contrib {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-2);
  line-height: 1.8;
}

/* ── Travel Modal ── */
.travel-modal { gap: var(--space-4); }

.travel-modal__header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.travel-modal__pin { font-size: 20px; }

.travel-modal__meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.travel-modal__meta-item {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
}

.travel-modal__field {
  display: flex;
  gap: var(--space-3);
  align-items: baseline;
}

.travel-modal__field-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-ink-3);
  flex-shrink: 0;
  min-width: 60px;
}

.travel-modal__field-value {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-2);
}

.travel-modal__journal {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.travel-modal__journal-text {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-2);
  line-height: 1.8;
}

.travel-modal__empty {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-3);
  font-style: italic;
}

@media (max-width: 767px) {
  .exp-card { flex-direction: column; }
  .exp-card__right { width: 100%; }
  .travel__body { flex-direction: column; }
  .travel__map { width: 100%; height: 280px; }
  .travel__continents { grid-template-columns: 1fr; }
}
</style>
