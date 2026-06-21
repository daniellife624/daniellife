<template>
  <div class="news-panel">
    <div class="search-bar">
      <input v-model="keyword" class="search-bar__input" type="text" placeholder="輸入新聞關鍵字" @keyup.enter="doSearch" />
      <button class="search-bar__btn" @click="doSearch" aria-label="搜尋">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
      </button>
    </div>

    <div class="region-tabs">
      <button
        v-for="tab in regionTabs"
        :key="tab.key"
        class="region-tab"
        :class="{ 'region-tab--active': region === tab.key }"
        @click="switchRegion(tab.key as NewsRegion)"
      >{{ tab.label }}</button>
    </div>

    <div class="news-list">
      <div v-if="loading" class="news-list__state">載入中…</div>
      <template v-else>
        <div v-if="!items.length" class="news-list__state">沒有符合的新聞</div>
        <NewsCard v-for="item in items" :key="item.id" :item="item" />
      </template>
    </div>

    <div class="pagination">
      <button class="pagination__btn" :disabled="page <= 1" @click="goPage(page - 1)">前一頁</button>
      <button
        v-for="p in totalPages"
        :key="p"
        class="pagination__num"
        :class="{ 'pagination__num--active': page === p }"
        @click="goPage(p)"
      >{{ p }}</button>
      <button class="pagination__btn" :disabled="page >= totalPages" @click="goPage(page + 1)">下一頁</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getNews } from '@/api/market'
import type { NewsItem, NewsRegion } from '@/types/market'
import NewsCard from '@/components/news/NewsCard.vue'

const region = ref<NewsRegion>('US')
const keyword = ref('')
const appliedKeyword = ref('')
const page = ref(1)
const items = ref<NewsItem[]>([])
const total = ref(0)
const loading = ref(false)

const PAGE_SIZE = 5
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)))

const regionTabs: { key: NewsRegion; label: string }[] = [
  { key: 'US',     label: 'US'     },
  { key: 'TAIWAN', label: 'TAIWAN' },
]

async function fetchNews() {
  loading.value = true
  const res = await getNews(region.value, page.value, appliedKeyword.value)
  items.value = res.items
  total.value = res.total
  loading.value = false
}

function doSearch() { appliedKeyword.value = keyword.value; page.value = 1; fetchNews() }
function switchRegion(r: NewsRegion) { region.value = r; page.value = 1; fetchNews() }
function goPage(p: number) { page.value = p; fetchNews() }

onMounted(() => fetchNews())
</script>

<style scoped>
.news-panel { flex: 1; display: flex; flex-direction: column; gap: var(--space-4); min-width: 0; }

.search-bar { display: flex; gap: 0; border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); overflow: hidden; transition: border-color 0.2s; }
.search-bar:focus-within { border-color: var(--color-ink-2); }

.search-bar__input { flex: 1; padding: var(--space-3) var(--space-4); border: none; background: var(--color-white); font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-1); outline: none; }
.search-bar__input::placeholder { color: var(--color-ink-3); }

.search-bar__btn { display: flex; align-items: center; justify-content: center; width: 48px; background: var(--color-ink-1); color: var(--color-white); border: none; cursor: pointer; transition: opacity 0.2s; flex-shrink: 0; }
.search-bar__btn:hover { opacity: 0.8; }

.region-tabs { display: flex; gap: 0; border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); overflow: hidden; width: fit-content; }
.region-tab { padding: var(--space-2) var(--space-6); background: var(--color-white); border: none; font-family: var(--font-body); font-size: 14px; font-weight: 600; color: var(--color-ink-2); cursor: pointer; letter-spacing: 0.04em; transition: background 0.15s, color 0.15s; }
.region-tab + .region-tab { border-left: 1px solid var(--color-ink-4); }
.region-tab--active { background: var(--color-primary); color: var(--color-ink-1); }

.news-list { display: flex; flex-direction: column; gap: var(--space-3); min-height: 320px; }
.news-list__state { font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-3); padding: var(--space-8) 0; text-align: center; }

.pagination { display: flex; justify-content: center; align-items: center; gap: var(--space-2); padding-top: var(--space-2); }
.pagination__btn { padding: var(--space-2) var(--space-4); background: var(--color-white); border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); cursor: pointer; transition: background 0.15s, color 0.15s; }
.pagination__btn:disabled { opacity: 0.35; cursor: default; }
.pagination__btn:not(:disabled):hover { background: var(--color-primary); color: var(--color-ink-1); border-color: var(--color-primary); }
.pagination__num { width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); background: var(--color-white); font-size: 13px; color: var(--color-ink-2); cursor: pointer; transition: background 0.15s, color 0.15s; }
.pagination__num--active { background: var(--color-primary); color: var(--color-ink-1); border-color: var(--color-primary); font-weight: 700; }
.pagination__num:not(.pagination__num--active):hover { background: rgba(232, 193, 58, 0.18); }
</style>
