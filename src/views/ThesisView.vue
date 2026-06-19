<template>
  <div class="thesis">
    <div class="thesis__inner">

      <!-- ── 碩論注意事項（collapsible）── -->
      <section class="thesis-section">
        <button class="collapsible-header" @click="noteOpen = !noteOpen">
          <span class="collapsible-header__title">碩論注意事項、教授建議</span>
          <span class="collapsible-header__arrow" :class="{ 'collapsible-header__arrow--open': noteOpen }">∨</span>
        </button>
        <div v-show="noteOpen" class="note-panel">
          <div v-if="!noteEditing" class="note-display">
            <p class="note-display__text">{{ note.content }}</p>
            <p class="note-display__date">上次更新：{{ note.updatedAt }}</p>
            <button class="note-btn" @click="startEdit">編輯</button>
          </div>
          <div v-else class="note-edit">
            <textarea v-model="editContent" class="note-edit__textarea" rows="6"></textarea>
            <div class="note-edit__actions">
              <button class="note-btn note-btn--cancel" @click="cancelEdit">取消</button>
              <button class="note-btn note-btn--save" @click="saveEdit">儲存</button>
            </div>
          </div>
        </div>
      </section>

      <!-- ── 碩論靈感 Kanban ── -->
      <section class="thesis-section">
        <div class="kanban-header">
          <h2 class="section-title">碩論靈感</h2>
          <button class="add-idea-btn" @click="showAddModal = true">＋ 新增便利貼</button>
        </div>
        <div class="kanban">
          <div v-for="col in kanbanCols" :key="col.status" class="kanban-col">
            <div class="kanban-col__header" :class="`kanban-col__header--${col.status}`">
              <span class="kanban-col__title">{{ col.label }}</span>
              <span class="kanban-col__count">{{ ideasByStatus(col.status).length }}</span>
            </div>
            <div
              class="kanban-col__body"
              :class="{ 'kanban-col__body--over': dragOverCol === col.status }"
              @dragover.prevent="dragOverCol = col.status"
              @dragleave="dragOverCol = null"
              @drop="onDrop($event, col.status)"
            >
              <p v-if="!ideasByStatus(col.status).length" class="kanban-empty">拖曳便利貼到此處</p>
              <div
                v-for="idea in ideasByStatus(col.status)"
                :key="idea.id"
                class="sticky-card"
                :class="{ 'sticky-card--dragging': draggingId === idea.id }"
                draggable="true"
                @dragstart="onDragStart($event, idea.id)"
                @dragend="draggingId = null; dragOverCol = null"
              >
                <div class="sticky-card__top">
                  <h4 class="sticky-card__title">{{ idea.title }}</h4>
                  <button class="sticky-card__del" @click.stop="deleteIdea(idea.id)">×</button>
                </div>
                <p class="sticky-card__content">{{ idea.content }}</p>
                <p class="sticky-card__date">{{ idea.createdAt }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── 參考文獻統整 ── -->
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
              <input
                v-model="paperKeyword"
                class="filter-input"
                type="text"
                placeholder="輸入論文關鍵字"
              />
              <button class="filter-search-btn">&#128269;</button>
            </div>
            <button class="notion-btn" @click="connectNotion">
              <span class="notion-btn__icon">N</span>
              連接 Notion 資料
            </button>
          </div>
        </div>
        <div class="papers-table-wrap">
          <table class="papers-table">
            <thead>
              <tr>
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
                <td class="paper-cell">
                  <span class="topic-badge">{{ p.topic }}</span>
                </td>
                <td class="paper-cell paper-cell--name">{{ p.name }}</td>
                <td class="paper-cell paper-cell--journal">{{ p.journal }}</td>
                <td class="paper-cell paper-cell--author">{{ p.authors }}, {{ p.year }}</td>
                <td class="paper-cell paper-cell--long">{{ p.purpose }}</td>
                <td class="paper-cell paper-cell--long">{{ p.contribution }}</td>
              </tr>
              <tr v-if="!filteredPapers.length">
                <td colspan="6" class="paper-cell paper-cell--empty">沒有符合的文獻</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

    </div>

    <!-- Add Idea Modal -->
    <Teleport to="body">
      <div v-if="showAddModal" class="modal-backdrop" @click.self="showAddModal = false">
        <div class="modal">
          <button class="modal__close" @click="showAddModal = false">×</button>
          <h3 class="modal__title">新增便利貼</h3>
          <label class="modal__label">
            標題
            <input v-model="newIdea.title" class="modal__input" type="text" placeholder="想法標題" />
          </label>
          <label class="modal__label">
            內容
            <textarea v-model="newIdea.content" class="modal__textarea" rows="4" placeholder="詳細描述這個研究方向…"></textarea>
          </label>
          <div class="modal__actions">
            <button class="modal__btn modal__btn--cancel" @click="showAddModal = false">取消</button>
            <button class="modal__btn modal__btn--add" @click="submitIdea">新增</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import {
  getThesisNote, saveThesisNote,
  getThesisIdeas, addThesisIdea, updateIdeaStatus, deleteThesisIdea,
  getThesisPapers,
} from '@/api/thesis'
import type { ThesisNote, ThesisIdea, ThesisPaper, IdeaStatus } from '@/types/thesis'

// ── Notes ──
const note        = ref<ThesisNote>({ content: '', updatedAt: '' })
const noteOpen    = ref(true)
const noteEditing = ref(false)
const editContent = ref('')

function startEdit()  { editContent.value = note.value.content; noteEditing.value = true }
function cancelEdit() { noteEditing.value = false }
async function saveEdit() {
  await saveThesisNote(editContent.value)
  note.value.content   = editContent.value
  note.value.updatedAt = new Date().toLocaleDateString('zh-TW')
  noteEditing.value    = false
}

// ── Kanban ──
const ideas = ref<ThesisIdea[]>([])
const kanbanCols: { status: IdeaStatus; label: string }[] = [
  { status: 'pending',  label: '待確認（重量提）' },
  { status: 'rejected', label: '被拒絕 / 不可執行' },
  { status: 'approved', label: '可以執行' },
]

function ideasByStatus(status: IdeaStatus) {
  return ideas.value.filter((i) => i.status === status)
}

async function changeStatus(id: number, status: IdeaStatus) {
  await updateIdeaStatus(id, status)
  const idea = ideas.value.find((i) => i.id === id)
  if (idea) idea.status = status
}

async function deleteIdea(id: number) {
  await deleteThesisIdea(id)
  ideas.value = ideas.value.filter((i) => i.id !== id)
}

// Drag and drop
const draggingId  = ref<number | null>(null)
const dragOverCol = ref<IdeaStatus | null>(null)

function onDragStart(e: DragEvent, id: number) {
  draggingId.value = id
  e.dataTransfer?.setData('text/plain', String(id))
  if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move'
}

async function onDrop(e: DragEvent, status: IdeaStatus) {
  e.preventDefault()
  const id = parseInt(e.dataTransfer?.getData('text/plain') ?? '')
  if (isNaN(id)) return
  dragOverCol.value = null
  await changeStatus(id, status)
}

// Add modal
const showAddModal = ref(false)
const newIdea = ref({ title: '', content: '', status: 'pending' as IdeaStatus, createdAt: '' })

async function submitIdea() {
  if (!newIdea.value.title.trim()) return
  const created = await addThesisIdea({ ...newIdea.value, createdAt: new Date().toISOString().slice(0, 10) })
  ideas.value.push(created)
  newIdea.value   = { title: '', content: '', status: 'pending', createdAt: '' }
  showAddModal.value = false
}

// ── Papers ──
const allPapers    = ref<ThesisPaper[]>([])
const paperKeyword = ref('')
const filterTopic  = ref('')
const filterJournal = ref('')

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

function connectNotion() {
  // TODO: Notion OAuth integration
  alert('Notion 整合功能開發中，敬請期待')
}

onMounted(async () => {
  note.value      = await getThesisNote()
  ideas.value     = await getThesisIdeas()
  allPapers.value = await getThesisPapers()
})
</script>

<style scoped>
.thesis {
  padding: var(--space-7) var(--space-6) var(--space-8);
  background: var(--color-white);
}

.thesis__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-7);
}

.thesis-section { display: flex; flex-direction: column; }

.section-title {
  font-family: var(--font-cjk);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-ink-1);
}

/* ── Collapsible ── */
.collapsible-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  background: var(--color-primary-bg);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-family: var(--font-cjk);
}

.collapsible-header__title { font-size: 16px; font-weight: 700; color: var(--color-ink-1); }
.collapsible-header__arrow { font-size: 14px; color: var(--color-ink-2); transition: transform 0.2s; }
.collapsible-header__arrow--open { transform: rotate(180deg); }

.note-panel {
  border: 1px solid var(--color-ink-4);
  border-top: none;
  border-radius: 0 0 var(--radius-md) var(--radius-md);
  padding: var(--space-4) var(--space-5);
}

.note-display { display: flex; flex-direction: column; gap: var(--space-3); }
.note-display__text { font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-2); line-height: 1.8; white-space: pre-wrap; }
.note-display__date { font-size: 12px; color: var(--color-ink-4); }

.note-edit { display: flex; flex-direction: column; gap: var(--space-3); }
.note-edit__textarea {
  width: 100%; padding: var(--space-3); border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 14px;
  resize: vertical; outline: none;
}
.note-edit__textarea:focus { border-color: var(--color-primary); }
.note-edit__actions { display: flex; gap: var(--space-2); justify-content: flex-end; }

.note-btn {
  padding: var(--space-2) var(--space-4); background: var(--color-ink-1); color: var(--color-white);
  border: none; border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 13px;
  cursor: pointer; transition: opacity 0.2s; align-self: flex-start;
}
.note-btn:hover { opacity: 0.8; }
.note-btn--cancel { background: var(--color-ink-4); color: var(--color-ink-1); }
.note-btn--save   { background: var(--color-primary); color: var(--color-ink-1); }

/* ── Kanban ── */
.kanban-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}

.add-idea-btn {
  padding: var(--space-2) var(--space-4); background: var(--color-ink-1); color: var(--color-white);
  border: none; border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 13px;
  font-weight: 600; cursor: pointer; transition: opacity 0.2s;
}
.add-idea-btn:hover { opacity: 0.8; }

.kanban { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.kanban-col { border: 1px solid var(--color-ink-4); border-radius: var(--radius-md); overflow: hidden; }

.kanban-col__header {
  padding: var(--space-3) var(--space-4);
  display: flex; align-items: center; justify-content: space-between;
}
.kanban-col__header--pending  { background: var(--color-primary-bg); border-bottom: 2px solid var(--color-primary); }
.kanban-col__header--rejected { background: #fef2f2; border-bottom: 2px solid #dc2626; }
.kanban-col__header--approved { background: #f0fdf4; border-bottom: 2px solid #16a34a; }

.kanban-col__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); }
.kanban-col__count {
  width: 22px; height: 22px; display: flex; align-items: center; justify-content: center;
  background: var(--color-ink-1); color: #fff; border-radius: 50%; font-size: 11px; font-weight: 700;
}

.kanban-col__body {
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  min-height: 140px;
  transition: background 0.15s;
}
.kanban-col__body--over { background: rgba(232, 193, 58, 0.08); }

.kanban-empty {
  font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-4);
  text-align: center; padding: var(--space-4) 0; border: 2px dashed var(--color-ink-4);
  border-radius: var(--radius-sm);
}

/* ── Sticky note cards ── */
.sticky-card {
  background: #fffde7;
  border-radius: var(--radius-sm);
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  cursor: grab;
  transition: opacity 0.2s, box-shadow 0.2s;
  user-select: none;
}
.sticky-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.13); }
.sticky-card--dragging { opacity: 0.4; cursor: grabbing; }

.sticky-card__top { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--space-2); }
.sticky-card__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); line-height: 1.4; }
.sticky-card__del { background: none; border: none; font-size: 16px; color: var(--color-ink-4); cursor: pointer; flex-shrink: 0; line-height: 1; padding: 0; }
.sticky-card__del:hover { color: #dc2626; }
.sticky-card__content {
  font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-2);
  line-height: 1.6;
  display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden;
}
.sticky-card__date { font-size: 11px; color: var(--color-ink-4); }

/* ── Papers ── */
.papers-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.papers-filters {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.filter-select-wrap {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}

.filter-select-label { white-space: nowrap; font-weight: 600; }

.filter-select {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  outline: none;
  cursor: pointer;
  background: var(--color-white);
  min-width: 100px;
}
.filter-select:focus { border-color: var(--color-primary); }

.filter-search { display: flex; }
.filter-input {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-right: none;
  border-radius: var(--radius-sm) 0 0 var(--radius-sm);
  font-family: var(--font-cjk); font-size: 13px;
  outline: none; width: 180px;
  transition: border-color 0.2s;
}
.filter-input:focus { border-color: var(--color-primary); }
.filter-search-btn {
  padding: var(--space-2) var(--space-3);
  background: var(--color-ink-1); color: #fff;
  border: 1px solid var(--color-ink-1);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  cursor: pointer; font-size: 13px; transition: opacity 0.2s;
}
.filter-search-btn:hover { opacity: 0.8; }

.notion-btn {
  display: flex; align-items: center; gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--color-ink-1); color: #fff;
  border: none; border-radius: var(--radius-sm);
  font-family: var(--font-cjk); font-size: 13px; font-weight: 600;
  cursor: pointer; transition: opacity 0.2s; white-space: nowrap;
}
.notion-btn:hover { opacity: 0.8; }

.notion-btn__icon {
  width: 18px; height: 18px;
  background: #fff; color: var(--color-ink-1);
  border-radius: 3px;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 900; font-family: var(--font-body);
  flex-shrink: 0;
}

.papers-table-wrap { overflow-x: auto; }

.papers-table { width: 100%; border-collapse: collapse; font-size: 13px; }

.papers-table th {
  padding: var(--space-3);
  background: var(--color-primary-bg);
  font-family: var(--font-cjk); font-weight: 700; color: var(--color-ink-1);
  border-bottom: 2px solid var(--color-primary);
  text-align: left; white-space: nowrap;
}

.col-topic        { width: 90px; }
.col-name         { min-width: 200px; }
.col-journal      { min-width: 160px; }
.col-author       { min-width: 140px; white-space: nowrap; }
.col-purpose      { min-width: 200px; }
.col-contribution { min-width: 220px; }

.paper-row:nth-child(even) { background: var(--color-primary-bg); }
.paper-row:hover { background: rgba(232, 193, 58, 0.18); }

.paper-cell {
  padding: var(--space-3); font-family: var(--font-cjk);
  color: var(--color-ink-2); border-bottom: 1px solid var(--color-ink-4);
  vertical-align: top; line-height: 1.6;
}

.paper-cell--name    { font-weight: 600; color: var(--color-ink-1); }
.paper-cell--journal { color: var(--color-secondary); font-weight: 600; }
.paper-cell--author  { white-space: nowrap; }
.paper-cell--long    { white-space: normal; }
.paper-cell--empty   { text-align: center; color: var(--color-ink-4); padding: var(--space-6) 0; }

.topic-badge {
  padding: 2px 8px;
  background: var(--color-primary-bg);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
  font-size: 12px; font-weight: 700; color: var(--color-ink-1);
  white-space: nowrap;
}

/* ── Add Modal ── */
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: var(--color-white); border-radius: var(--radius-md); padding: var(--space-6); width: 480px; max-width: 90vw; position: relative; display: flex; flex-direction: column; gap: var(--space-4); }
.modal__close { position: absolute; top: var(--space-4); right: var(--space-4); font-size: 20px; background: none; border: none; cursor: pointer; color: var(--color-ink-3); }
.modal__title { font-family: var(--font-cjk); font-size: 18px; font-weight: 700; color: var(--color-ink-1); }
.modal__label { display: flex; flex-direction: column; gap: var(--space-1); font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); }
.modal__input, .modal__textarea {
  padding: var(--space-2) var(--space-3); border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 14px;
  outline: none; width: 100%; box-sizing: border-box; transition: border-color 0.2s;
}
.modal__input:focus, .modal__textarea:focus { border-color: var(--color-primary); }
.modal__textarea { resize: vertical; }
.modal__actions { display: flex; gap: var(--space-2); justify-content: flex-end; }
.modal__btn { padding: var(--space-2) var(--space-5); border: none; border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 14px; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
.modal__btn:hover { opacity: 0.82; }
.modal__btn--cancel { background: var(--color-ink-4); color: var(--color-ink-1); }
.modal__btn--add    { background: var(--color-primary); color: var(--color-ink-1); }

@media (max-width: 767px) {
  .kanban { grid-template-columns: 1fr; }
  .papers-header { flex-direction: column; align-items: flex-start; }
  .papers-filters { width: 100%; }
  .filter-input { width: 140px; }
}
</style>
