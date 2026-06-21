<template>
  <div class="activities">

    <!-- 領導經驗 -->
    <section class="exp-section">
      <div class="exp-section__inner">
        <h2 class="page-title">領導經驗</h2>
        <div class="exp-list">
          <ExperienceCard
            v-for="item in leadershipItems"
            :key="item.id"
            :item="item"
            @view-more="activeModal = item"
          />
        </div>
      </div>
    </section>

    <!-- 社團經驗 -->
    <section class="exp-section exp-section--alt">
      <div class="exp-section__inner">
        <h2 class="page-title">社團經驗</h2>
        <div class="exp-list">
          <ExperienceCard
            v-for="item in clubItems"
            :key="item.id"
            :item="item"
            @view-more="activeModal = item"
          />
        </div>
      </div>
    </section>

    <!-- 造訪過國家 -->
    <section class="travel">
      <div class="travel__inner">
        <h2 class="page-title">造訪過國家</h2>
        <p class="travel__subtitle">丹尼的旅行日記 / 讓知識不再僅限於課本</p>
        <div class="travel__body">
          <div class="travel__map" ref="mapEl"></div>
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

    <ExperienceModal :experience="activeModal" @close="activeModal = null" />
    <TravelEntryModal :entry="activeTravelEntry" @close="activeTravelEntry = null" />
    <AddTravelModal
      :continent="addEntryCont"
      :accent-bg="addEntryColor.bg"
      :accent-text="addEntryColor.text"
      @close="addEntryCont = null"
      @submitted="onEntrySubmitted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import * as topojson from 'topojson-client'
import { getExperiences, getTravelEntries, groupByContinent } from '@/api/activities'
import type { Experience, TravelEntry, Continent } from '@/types/activities'
import ExperienceCard from '@/components/activities/ExperienceCard.vue'
import ExperienceModal from '@/components/activities/ExperienceModal.vue'
import TravelEntryModal from '@/components/activities/TravelEntryModal.vue'
import AddTravelModal from '@/components/activities/AddTravelModal.vue'

const experiences = ref<Experience[]>([])
const activeModal = ref<Experience | null>(null)
const activeTravelEntry = ref<TravelEntry | null>(null)
const mapEl = ref<HTMLElement | null>(null)
let leafletMap: L.Map | null = null

const leadershipItems = computed(() => experiences.value.filter((e) => e.type === 'leadership'))
const clubItems = computed(() => experiences.value.filter((e) => e.type === 'club'))
const continents = ref(groupByContinent([]))

const CONT_COLORS: Record<string, { bg: string; text: string }> = {
  Europe:    { bg: '#2563eb', text: '#fff' },
  Asia:      { bg: '#E8C13A', text: '#1a1a1a' },
  Africa:    { bg: '#303030', text: '#fff' },
  Australia: { bg: '#0d9488', text: '#fff' },
  Americas:  { bg: '#C17055', text: '#fff' },
}

const addEntryCont  = ref<Continent | null>(null)
const addEntryColor = ref({ bg: '#3b82f6', text: '#fff' })

function openAddEntry(cont: Continent) {
  addEntryCont.value  = cont
  addEntryColor.value = CONT_COLORS[cont.key] ?? { bg: '#3b82f6', text: '#fff' }
}

async function onEntrySubmitted() {
  const entries = await getTravelEntries()
  continents.value = groupByContinent(entries)
  if (leafletMap) { leafletMap.remove(); leafletMap = null }
  await initMap(entries)
}

const COUNTRY_CODES: Record<string, number> = {
  '臺灣': 158, '台灣': 158,
  '日本': 392, '澳大利亞': 36, '美國': 840, '英國': 826,
  '法國': 250, '德國': 276, '韓國': 410, '中國': 156,
  '泰國': 764, '新加坡': 702, '義大利': 380, '西班牙': 724, '加拿大': 124,
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
    zoomControl: true, dragging: true, scrollWheelZoom: false,
    doubleClickZoom: true, touchZoom: true, attributionControl: false,
    center: [20, 20], zoom: 2, minZoom: 1, maxZoom: 8,
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
          color: '#ffffff', weight: 0.6, opacity: 1,
          className: visited ? 'map-country--visited' : '',
        }
      },
      onEachFeature: (feature, layer) => {
        const id = Number(feature?.id)
        if (!visitedNums.has(id)) return
        const entry = codeToEntry.get(id)
        layer.on('mouseover', () => { ;(layer as L.Path).setStyle({ fillColor: '#c9a500', fillOpacity: 1 }) })
        layer.on('mouseout',  () => { ;(layer as L.Path).setStyle({ fillColor: '#E8C13A', fillOpacity: 0.88 }) })
        layer.on('click',     () => { if (entry) activeTravelEntry.value = entry })
      },
    }).addTo(leafletMap)
  } catch { /* silent */ }
}

onMounted(async () => {
  experiences.value = await getExperiences()
  const entries = await getTravelEntries()
  continents.value = groupByContinent(entries)
  await initMap(entries)
})

onUnmounted(() => { leafletMap?.remove(); leafletMap = null })
</script>

<style scoped>
.activities { background-color: var(--color-white); }

.exp-section { padding: var(--space-8) var(--space-6); }
.exp-section--alt { background-color: #fafafa; border-top: 1px solid var(--color-ink-4); }
.exp-section__inner { max-width: var(--container-max); margin: 0 auto; }

.page-title {
  font-family: var(--font-cjk);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-ink-1);
  margin-bottom: var(--space-5);
}

.exp-list { display: flex; flex-direction: column; gap: var(--space-5); }

.travel { padding: var(--space-8) var(--space-6); border-top: 1px solid var(--color-ink-4); }
.travel__inner { max-width: var(--container-max); margin: 0 auto; }

.travel__subtitle {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-3);
  margin-bottom: var(--space-6);
}

.travel__body { display: flex; gap: var(--space-6); align-items: flex-start; }

.travel__map {
  flex-shrink: 0;
  width: 440px;
  height: 380px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-ink-4);
  background-color: #e8f0f8;
}

.travel__map :deep(.map-country--visited) { cursor: pointer; }

.travel__continents { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); flex: 1; }

.continent-card {
  border-radius: var(--radius-md);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  border: 1px solid var(--color-ink-4);
}

.continent-card__title { font-family: var(--font-body); font-size: 14px; font-weight: 700; }

.continent-card--europe    .continent-card__title { color: #2563eb; }
.continent-card--asia      .continent-card__title { color: var(--color-primary); }
.continent-card--africa    .continent-card__title { color: var(--color-ink-1); }
.continent-card--australia .continent-card__title { color: #0d9488; }
.continent-card--americas  .continent-card__title { color: var(--color-tertiary); }

.continent-card__list { list-style: none; flex: 1; }

.continent-card__empty { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-3); }

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

.continent-card--europe    .continent-card__btn { background: #2563eb; color: #fff; }
.continent-card--asia      .continent-card__btn { background: var(--color-primary); color: var(--color-ink-1); }
.continent-card--africa    .continent-card__btn { background: var(--color-ink-1); color: #fff; }
.continent-card--australia .continent-card__btn { background: #0d9488; color: #fff; }
.continent-card--americas  .continent-card__btn { background: var(--color-tertiary); color: #fff; }

@media (max-width: 1024px) {
  .travel__map { width: 100%; height: 320px; }
  .travel__body { flex-direction: column; }
}

@media (max-width: 767px) {
  .travel__continents { grid-template-columns: 1fr; }
}
</style>
