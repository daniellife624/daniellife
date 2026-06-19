<template>
  <div class="news">
    <div class="news__inner">

      <!-- Left: News Panel -->
      <div class="news-panel">

        <!-- Search bar -->
        <div class="search-bar">
          <input
            v-model="keyword"
            class="search-bar__input"
            type="text"
            placeholder="輸入新聞關鍵字"
            @keyup.enter="doSearch"
          />
          <button class="search-bar__btn" @click="doSearch" aria-label="搜尋">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
          </button>
        </div>

        <!-- Region tabs -->
        <div class="region-tabs">
          <button
            v-for="tab in regionTabs"
            :key="tab.key"
            class="region-tab"
            :class="{ 'region-tab--active': region === tab.key }"
            @click="switchRegion(tab.key as NewsRegion)"
          >{{ tab.label }}</button>
        </div>

        <!-- News list -->
        <div class="news-list">
          <div v-if="loading" class="news-list__state">載入中…</div>
          <template v-else>
            <div v-if="!items.length" class="news-list__state">沒有符合的新聞</div>
            <a
              v-for="item in items"
              :key="item.id"
              :href="item.url || '#'"
              :target="item.url ? '_blank' : '_self'"
              rel="noopener"
              class="news-card"
            >
              <h3 class="news-card__title">{{ item.title }}</h3>
              <p class="news-card__summary">{{ item.summary }}</p>
              <div class="news-card__footer">
                <time class="news-card__time">{{ item.publishedAt }}</time>
                <span class="news-card__source">{{ item.source }}</span>
              </div>
            </a>
          </template>
        </div>

        <!-- Pagination -->
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

      <!-- Right: Chatbot Panel -->
      <div class="chat-panel">
        <div class="chat-panel__header">
          <div class="chat-panel__brand">
            <span class="chat-panel__d">D</span>
            <span class="chat-panel__title">Daniellife 會計丹尼</span>
          </div>
          <span class="chat-panel__model">使用模型：&#123;ChatGPT 4.0&#125;</span>
        </div>

        <div class="chat-panel__messages" ref="messagesEl">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="chat-msg"
            :class="`chat-msg--${msg.role}`"
          >
            <div class="chat-msg__bubble">{{ msg.content }}</div>
          </div>
          <div v-if="!messages.length" class="chat-panel__hint">
            詢問任何財經問題<br>例如：「幫我解釋 Fed 升息對台股的影響」
          </div>
        </div>

        <div class="chat-panel__input-row">
          <input
            v-model="chatInput"
            class="chat-panel__input"
            type="text"
            placeholder="輸入……"
            @keyup.enter="sendChat"
          />
          <button class="chat-panel__send" @click="sendChat" aria-label="送出">▶</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { getNews } from '@/api/market'
import type { NewsItem, NewsRegion, ChatMessage } from '@/types/market'

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

function doSearch() {
  appliedKeyword.value = keyword.value
  page.value = 1
  fetchNews()
}

function switchRegion(r: NewsRegion) {
  region.value = r
  page.value = 1
  fetchNews()
}

function goPage(p: number) {
  page.value = p
  fetchNews()
}

onMounted(() => fetchNews())

// ── Chatbot (UI only) ──
const messages = ref<ChatMessage[]>([])
const chatInput = ref('')
const messagesEl = ref<HTMLElement | null>(null)

async function sendChat() {
  const text = chatInput.value.trim()
  if (!text) return
  chatInput.value = ''
  messages.value.push({ role: 'user', content: text })
  // TODO: call GitHub Models API (GPT-4o) here
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  setTimeout(() => {
    messages.value.push({ role: 'assistant', content: '（AI 回覆功能尚未串接，敬請期待）' })
    nextTick(() => {
      if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
    })
  }, 600)
}
</script>

<style scoped>
.news {
  padding: var(--space-6) var(--space-6) var(--space-8);
  background: var(--color-white);
  min-height: calc(100vh - 64px);
}

.news__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  display: flex;
  gap: var(--space-6);
  align-items: flex-start;
}

/* ── News Panel ── */
.news-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  min-width: 0;
}

/* Search bar */
.search-bar {
  display: flex;
  gap: 0;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  overflow: hidden;
  transition: border-color 0.2s;
}
.search-bar:focus-within { border-color: var(--color-ink-2); }

.search-bar__input {
  flex: 1;
  padding: var(--space-3) var(--space-4);
  border: none;
  background: var(--color-white);
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-1);
  outline: none;
}
.search-bar__input::placeholder { color: var(--color-ink-3); }

.search-bar__btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  background: var(--color-ink-1);
  color: var(--color-white);
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
  flex-shrink: 0;
}
.search-bar__btn:hover { opacity: 0.8; }

/* Region tabs — pill toggle */
.region-tabs {
  display: flex;
  gap: 0;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  overflow: hidden;
  width: fit-content;
}

.region-tab {
  padding: var(--space-2) var(--space-6);
  background: var(--color-white);
  border: none;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-ink-2);
  cursor: pointer;
  letter-spacing: 0.04em;
  transition: background 0.15s, color 0.15s;
}
.region-tab + .region-tab { border-left: 1px solid var(--color-ink-4); }
.region-tab--active {
  background: var(--color-primary);
  color: var(--color-ink-1);
}

/* News list */
.news-list { display: flex; flex-direction: column; gap: var(--space-3); min-height: 320px; }

.news-list__state {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-3);
  padding: var(--space-8) 0;
  text-align: center;
}

/* News card */
.news-card {
  display: block;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
  text-decoration: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.news-card:hover {
  border-color: var(--color-primary);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.news-card__title {
  font-family: var(--font-cjk);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-ink-1);
  line-height: 1.5;
  margin-bottom: var(--space-2);
}

.news-card__summary {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: var(--space-3);
}

.news-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.news-card__time {
  font-size: 12px;
  color: var(--color-ink-3);
  font-family: var(--font-body);
}

.news-card__source {
  font-size: 11px;
  font-weight: 600;
  background: var(--color-secondary);
  color: var(--color-white);
  padding: 2px 8px;
  border-radius: 3px;
  letter-spacing: 0.02em;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-2);
  padding-top: var(--space-2);
}

.pagination__btn {
  padding: var(--space-2) var(--space-4);
  background: var(--color-white);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.pagination__btn:disabled { opacity: 0.35; cursor: default; }
.pagination__btn:not(:disabled):hover { background: var(--color-primary); color: var(--color-ink-1); border-color: var(--color-primary); }

.pagination__num {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  background: var(--color-white);
  font-size: 13px;
  color: var(--color-ink-2);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.pagination__num--active {
  background: var(--color-primary);
  color: var(--color-ink-1);
  border-color: var(--color-primary);
  font-weight: 700;
}
.pagination__num:not(.pagination__num--active):hover {
  background: rgba(232, 193, 58, 0.18);
}

/* ── Chat Panel ── */
.chat-panel {
  flex-shrink: 0;
  width: 360px;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  height: 620px;
  overflow: hidden;
  position: sticky;
  top: var(--space-6);
}

.chat-panel__header {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-ink-4);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--color-white);
  flex-shrink: 0;
}

.chat-panel__brand {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.chat-panel__d {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: var(--color-ink-1);
  line-height: 1;
  flex-shrink: 0;
}

.chat-panel__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); }
.chat-panel__model { font-size: 11px; color: var(--color-ink-3); font-family: var(--font-body); }

.chat-panel__messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.chat-panel__hint {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
  text-align: center;
  padding-top: var(--space-6);
  line-height: 1.9;
}

.chat-msg { display: flex; }
.chat-msg--user      { justify-content: flex-end; }
.chat-msg--assistant { justify-content: flex-start; }

.chat-msg__bubble {
  max-width: 82%;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-family: var(--font-cjk);
  font-size: 13px;
  line-height: 1.7;
}
.chat-msg--user .chat-msg__bubble {
  background: rgba(232, 193, 58, 0.28);
  color: var(--color-ink-1);
  border-bottom-right-radius: 4px;
}
.chat-msg--assistant .chat-msg__bubble {
  background: rgba(232, 193, 58, 0.13);
  color: var(--color-ink-1);
  border-bottom-left-radius: 4px;
}

.chat-panel__input-row {
  border-top: 1px solid var(--color-ink-4);
  padding: var(--space-3);
  display: flex;
  gap: var(--space-2);
  flex-shrink: 0;
}

.chat-panel__input {
  flex: 1;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-1);
  outline: none;
  transition: border-color 0.2s;
}
.chat-panel__input:focus { border-color: var(--color-primary); }
.chat-panel__input::placeholder { color: var(--color-ink-3); }

.chat-panel__send {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius-sm);
  font-size: 15px;
  color: var(--color-ink-1);
  cursor: pointer;
  transition: opacity 0.2s;
  flex-shrink: 0;
}
.chat-panel__send:hover { opacity: 0.82; }

@media (max-width: 960px) {
  .news__inner { flex-direction: column; }
  .chat-panel { width: 100%; position: static; height: 480px; }
}
</style>
