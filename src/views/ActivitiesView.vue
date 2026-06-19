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
          <!-- Leaflet 世界地圖 -->
          <div class="travel__map" ref="mapEl"></div>
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
              <button
                class="continent-card__btn"
                :class="`continent-card__btn--${cont.key.toLowerCase()}`"
                @click="openAddEntry(cont)"
              >
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

    <!-- 新增旅行日記 Modal -->
    <Teleport to="body">
      <div v-if="addEntryCont" class="modal-backdrop" @click.self="addEntryCont = null">
        <div
          class="modal add-modal"
          :style="{ '--accent': addEntryColor.bg, '--accent-text': addEntryColor.text }"
        >
          <button class="modal__close" @click="addEntryCont = null">×</button>

          <div class="add-modal__header">
            <span class="add-modal__pre">地區（自動帶入）：</span>
            <span class="add-modal__cont">{{ CONT_ZH[addEntryCont.key] || addEntryCont.label }}</span>
          </div>

          <!-- 人事時地物 -->
          <div class="add-modal__fields">
            <div class="add-modal__row">
              <div class="add-modal__icon">人</div>
              <input class="add-modal__input" placeholder="和誰一起去？" v-model="newEntry.companions" />
            </div>
            <div class="add-modal__row">
              <div class="add-modal__icon">事</div>
              <input class="add-modal__input" placeholder="做了什麼有趣的事情？" v-model="newEntry.activities" />
            </div>
            <div class="add-modal__row">
              <div class="add-modal__icon">時</div>
              <input class="add-modal__input" placeholder="詳細的時間點？（e.g. 2024-03）" v-model="newEntry.visitedAt" />
            </div>
            <div class="add-modal__row">
              <div class="add-modal__icon">地</div>
              <input
                class="add-modal__input"
                :placeholder="`去 ${CONT_ZH[addEntryCont.key] || addEntryCont.label} 的哪個國家？哪座城市？`"
                v-model="newEntry.city"
              />
            </div>
            <div class="add-modal__row">
              <div class="add-modal__icon">物</div>
              <input class="add-modal__input" placeholder="有沒有買什麼東西？" v-model="newEntry.purchases" />
            </div>
          </div>

          <!-- 照片上傳 -->
          <div class="add-modal__photos">
            <div
              v-for="(photo, i) in newPhotos"
              :key="i"
              class="add-modal__photo-slot"
              @click="triggerPhoto(i)"
            >
              <img v-if="photo" :src="photo" class="add-modal__photo-img" alt="旅行照片" />
              <span v-else class="add-modal__photo-add">+</span>
            </div>
          </div>
          <input ref="photoInputEl" type="file" accept="image/*" style="display:none" @change="onPhotoChange" />

          <button class="add-modal__submit" @click="submitAddEntry">新增旅行日記</button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, reactive } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import * as topojson from 'topojson-client'
import { getExperiences, getTravelEntries, groupByContinent } from '@/api/activities'
import type { Experience, TravelEntry, Continent } from '@/types/activities'

const experiences = ref<Experience[]>([])
const activeModal = ref<Experience | null>(null)
const activeTravelEntry = ref<TravelEntry | null>(null)
const mapEl = ref<HTMLElement | null>(null)
let leafletMap: L.Map | null = null

/* ── 新增旅行日記 popup ── */
const CONT_ZH: Record<string, string> = {
  Europe: '歐洲', Asia: '亞洲', Africa: '非洲',
  Australia: '澳洲', Americas: '美洲',
}

const CONT_COLORS: Record<string, { bg: string; text: string }> = {
  Europe:    { bg: '#2563eb', text: '#fff' },
  Asia:      { bg: '#E8C13A', text: '#1a1a1a' },
  Africa:    { bg: '#303030', text: '#fff' },
  Australia: { bg: '#0d9488', text: '#fff' },
  Americas:  { bg: '#C17055', text: '#fff' },
}

const addEntryCont  = ref<Continent | null>(null)
const addEntryColor = ref({ bg: '#3b82f6', text: '#fff' })
const newEntry = reactive({ companions: '', activities: '', visitedAt: '', city: '', purchases: '' })
const newPhotos = ref<(string | null)[]>([null, null, null, null])
let currentPhotoSlot = 0
const photoInputEl = ref<HTMLInputElement | null>(null)

function openAddEntry(cont: Continent) {
  addEntryCont.value  = cont
  addEntryColor.value = CONT_COLORS[cont.key] ?? { bg: '#3b82f6', text: '#fff' }
  Object.assign(newEntry, { companions: '', activities: '', visitedAt: '', city: '', purchases: '' })
  newPhotos.value = [null, null, null, null]
}

function triggerPhoto(i: number) {
  currentPhotoSlot = i
  photoInputEl.value?.click()
}

function onPhotoChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  newPhotos.value[currentPhotoSlot] = URL.createObjectURL(file)
  ;(e.target as HTMLInputElement).value = ''
}

function submitAddEntry() {
  // TODO: POST to backend — for now close modal
  addEntryCont.value = null
}

const leadershipItems = computed(() => experiences.value.filter((e) => e.type === 'leadership'))
const clubItems = computed(() => experiences.value.filter((e) => e.type === 'club'))

const continents = ref(groupByContinent([]))

/* ISO 3166-1 numeric codes for visited countries */
const COUNTRY_CODES: Record<string, number> = {
  '臺灣': 158, '台灣': 158,
  '日本': 392,
  '澳大利亞': 36,
  '美國': 840,
  '英國': 826,
  '法國': 250,
  '德國': 276,
  '韓國': 410,
  '中國': 156,
  '泰國': 764,
  '新加坡': 702,
  '義大利': 380,
  '西班牙': 724,
  '加拿大': 124,
}

async function initMap(entries: TravelEntry[]) {
  if (!mapEl.value) return

  const visitedNums = new Set(entries.map((e) => COUNTRY_CODES[e.country]).filter(Boolean))
  const codeToEntry = new Map<number, TravelEntry>()
  for (const e of entries) {
    const code = COUNTRY_CODES[e.country]
    if (code) codeToEntry.set(code, e)
  }

  leafletMap = L.map(mapEl.value, {
    zoomControl: true,
    dragging: true,
    scrollWheelZoom: false,   // 不攔截頁面滾動
    doubleClickZoom: true,
    touchZoom: true,
    attributionControl: false,
    center: [20, 20],
    zoom: 2,
    minZoom: 1,
    maxZoom: 8,
  })

  try {
    const res = await fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
    const world = (await res.json()) as any
    const geo = topojson.feature(world, world.objects.countries) as any

    L.geoJSON(geo, {
      style: (feature) => {
        const id = Number(feature?.id)
        const visited = visitedNums.has(id)
        return {
          fillColor: visited ? '#E8C13A' : '#d1d5db',
          fillOpacity: visited ? 0.88 : 0.45,
          color: '#ffffff',
          weight: 0.6,
          opacity: 1,
          className: visited ? 'map-country--visited' : '',
        }
      },
      onEachFeature: (feature, layer) => {
        const id = Number(feature?.id)
        if (!visitedNums.has(id)) return

        const entry = codeToEntry.get(id)

        layer.on('mouseover', () => {
          ;(layer as L.Path).setStyle({ fillColor: '#c9a500', fillOpacity: 1 })
        })
        layer.on('mouseout', () => {
          ;(layer as L.Path).setStyle({ fillColor: '#E8C13A', fillOpacity: 0.88 })
        })
        layer.on('click', () => {
          if (entry) activeTravelEntry.value = entry
        })
      },
    }).addTo(leafletMap)
  } catch {
    /* silently keep blank map on fetch failure */
  }
}

onMounted(async () => {
  experiences.value = await getExperiences()
  const entries = await getTravelEntries()
  continents.value = groupByContinent(entries)
  await initMap(entries)
})

onUnmounted(() => {
  leafletMap?.remove()
  leafletMap = null
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
  width: 440px;
  height: 380px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-ink-4);
  background-color: #e8f0f8;
}

/* 訪過的國家滑鼠指標 */
.travel__map :deep(.map-country--visited) {
  cursor: pointer;
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

/* ── 新增旅行日記 Modal ── */
.add-modal {
  max-width: 500px;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
}

.add-modal__header {
  font-family: var(--font-cjk);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-ink-1);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  padding-right: var(--space-5);
  margin-bottom: 2px;
}

.add-modal__pre { font-weight: 400; }
.add-modal__cont { color: var(--accent, #3b82f6); }

.add-modal__fields {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.add-modal__row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.add-modal__icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--accent, #3b82f6);
  color: var(--accent-text, #fff);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.add-modal__input {
  flex: 1;
  border: none;
  border-bottom: 1px solid var(--color-ink-4);
  outline: none;
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-1);
  padding: 5px 2px;
  background: transparent;
  transition: border-color 0.2s;
}

.add-modal__input:focus { border-bottom-color: var(--accent, #3b82f6); }
.add-modal__input::placeholder { color: var(--color-ink-3); }

.add-modal__photos {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2);
}

.add-modal__photo-slot {
  height: 100px;
  border: 2px dashed var(--color-ink-4);
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: border-color 0.2s;
}

.add-modal__photo-slot:hover { border-color: var(--accent, #3b82f6); }

.add-modal__photo-add {
  font-size: 28px;
  color: var(--color-ink-4);
  line-height: 1;
}

.add-modal__photo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.add-modal__submit {
  width: 100%;
  padding: var(--space-3) 0;
  background: var(--accent, #3b82f6);
  color: var(--accent-text, #fff);
  font-family: var(--font-cjk);
  font-size: 15px;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: opacity 0.2s;
}

.add-modal__submit:hover { opacity: 0.88; }

@media (max-width: 1024px) {
  .travel__map { width: 100%; height: 320px; }
  .travel__body { flex-direction: column; }
}

@media (max-width: 767px) {
  .exp-card { flex-direction: column; }
  .exp-card__right { width: 100%; }
  .travel__continents { grid-template-columns: 1fr; }
}
</style>
