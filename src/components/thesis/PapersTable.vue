<template>
  <section class="thesis-section">
    <div class="papers-header">
      <h2 class="section-title">參考文獻統整</h2>
      <div class="papers-filters">
        <label class="filter-select-wrap">
          <span class="filter-select-label">Topic：</span>
          <select v-model="filterTopic" class="filter-select">
            <option value="">全部</option>
            <option v-for="t in topicOptions" :key="t" :value="t">{{ t }}</option>
          </select>
        </label>
        <label class="filter-select-wrap">
          <span class="filter-select-label">Journal：</span>
          <select v-model="filterJournal" class="filter-select">
            <option value="">全部</option>
            <option v-for="j in journalOptions" :key="j" :value="j">{{ j }}</option>
          </select>
        </label>
        <div class="filter-search">
          <input v-model="paperKeyword" class="filter-input" type="text" placeholder="輸入論文關鍵字" />
          <button class="filter-search-btn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
    <div class="papers-table-wrap">
      <table class="papers-table">
        <thead>
          <tr>
            <th class="col-notes">筆記</th>
            <th class="col-topic">Topic</th>
            <th class="col-name">Name</th>
            <th class="col-journal">Journal</th>
            <th class="col-author">Author, Year</th>
            <th class="col-purpose">研究目的（150字）</th>
            <th class="col-contribution">研究貢獻／影響／結果（200字／項目符號）</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in filteredPapers" :key="p.id" class="paper-row">
            <td class="paper-cell paper-cell--notes">
              <button class="note-btn" :class="{ 'note-btn--filled': p.notes }" @click="notePaper = p">
                {{ p.notes ? '查看筆記' : '尚無筆記' }}
              </button>
            </td>
            <td class="paper-cell"><span class="topic-badge">{{ p.topic }}</span></td>
            <td class="paper-cell paper-cell--name">{{ p.name }}</td>
            <td class="paper-cell paper-cell--journal">{{ p.journal }}</td>
            <td class="paper-cell paper-cell--author">{{ p.authors }}, {{ p.year }}</td>
            <td class="paper-cell paper-cell--long">{{ p.purpose }}</td>
            <td class="paper-cell paper-cell--long">{{ p.contribution }}</td>
          </tr>
          <tr v-if="!filteredPapers.length">
            <td colspan="7" class="paper-cell paper-cell--empty">沒有符合的文獻</td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaperNoteModal :paper="notePaper" @close="notePaper = null" />
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getThesisPapers } from '@/api/thesis'
import PaperNoteModal from './PaperNoteModal.vue'
import type { ThesisPaper } from '@/types/thesis'

const allPapers    = ref<ThesisPaper[]>([])
const paperKeyword = ref('')
const filterTopic  = ref('')
const filterJournal = ref('')
const notePaper    = ref<ThesisPaper | null>(null)

const topicOptions   = computed(() => [...new Set(allPapers.value.map((p) => p.topic))].filter(Boolean))
const journalOptions = computed(() => [...new Set(allPapers.value.map((p) => p.journal))].filter(Boolean))

const filteredPapers = computed(() =>
  allPapers.value.filter((p) => {
    const kw = paperKeyword.value.toLowerCase()
    return (
      (!filterTopic.value   || p.topic   === filterTopic.value) &&
      (!filterJournal.value || p.journal === filterJournal.value) &&
      (!kw || p.name.toLowerCase().includes(kw) || p.purpose.toLowerCase().includes(kw) || p.contribution.toLowerCase().includes(kw))
    )
  })
)

onMounted(async () => { allPapers.value = await getThesisPapers() })
</script>

<style scoped>
.thesis-section { display: flex; flex-direction: column; }
.section-title { font-family: var(--font-cjk); font-size: 20px; font-weight: 700; color: var(--color-ink-1); }

.papers-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-4); flex-wrap: wrap; gap: var(--space-3); }
.papers-filters { display: flex; align-items: center; gap: var(--space-3); flex-wrap: wrap; }

.filter-select-wrap { display: flex; align-items: center; gap: var(--space-1); font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); }
.filter-select-label { white-space: nowrap; font-weight: 600; }
.filter-select { padding: var(--space-2) var(--space-3); border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 13px; outline: none; cursor: pointer; background: var(--color-white); min-width: 100px; }
.filter-select:focus { border-color: var(--color-primary); }

.filter-search { display: flex; }
.filter-input { padding: var(--space-2) var(--space-3); border: 1px solid var(--color-ink-4); border-right: none; border-radius: var(--radius-sm) 0 0 var(--radius-sm); font-family: var(--font-cjk); font-size: 13px; outline: none; width: 180px; transition: border-color 0.2s; }
.filter-input:focus { border-color: var(--color-primary); }
.filter-search-btn { padding: var(--space-2) var(--space-3); background: var(--color-ink-1); color: #fff; border: 1px solid var(--color-ink-1); border-radius: 0 var(--radius-sm) var(--radius-sm) 0; cursor: pointer; font-size: 13px; transition: opacity 0.2s; }
.filter-search-btn:hover { opacity: 0.8; }


.papers-table-wrap { overflow-x: auto; }
.papers-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.papers-table th { padding: var(--space-3); background: var(--color-primary-bg); font-family: var(--font-cjk); font-weight: 700; color: var(--color-ink-1); border-bottom: 2px solid var(--color-primary); text-align: left; white-space: nowrap; }

.col-topic { width: 90px; }
.col-name { min-width: 200px; }
.col-journal { min-width: 160px; }
.col-author { min-width: 140px; white-space: nowrap; }
.col-purpose { min-width: 200px; }
.col-contribution { min-width: 220px; }
.col-notes { width: 100px; }

.paper-row:nth-child(even) { background: var(--color-primary-bg); }
.paper-row:hover { background: #e8e8e8; }

.paper-cell { padding: var(--space-3); font-family: var(--font-cjk); color: var(--color-ink-2); border-bottom: 1px solid var(--color-ink-4); vertical-align: top; line-height: 1.6; }
.paper-cell--name { font-weight: 600; color: var(--color-ink-1); }
.paper-cell--journal { color: var(--color-secondary); font-weight: 600; }
.paper-cell--author { white-space: nowrap; }
.paper-cell--long { white-space: normal; }
.paper-cell--empty { text-align: center; color: var(--color-ink-4); padding: var(--space-6) 0; }
.paper-cell--notes { white-space: nowrap; }

.note-btn { padding: var(--space-1) var(--space-3); border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); background: var(--color-white); font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-2); cursor: pointer; transition: border-color 0.15s, color 0.15s; }
.note-btn:hover { border-color: var(--color-ink-1); color: var(--color-ink-1); }
.note-btn--filled { border-color: var(--color-primary); color: var(--color-ink-1); font-weight: 600; background: var(--color-primary-bg); }

.topic-badge { padding: 2px 8px; background: var(--color-primary-bg); border: 1px solid var(--color-primary); border-radius: var(--radius-sm); font-size: 12px; font-weight: 700; color: var(--color-ink-1); white-space: nowrap; }

@media (max-width: 767px) { .papers-header { flex-direction: column; align-items: flex-start; } .papers-filters { width: 100%; } .filter-input { width: 140px; } }
</style>
