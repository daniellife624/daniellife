<template>
  <div class="thesis">
    <div class="thesis__inner">

      <!-- ── Notes Section (collapsible) ── -->
      <section class="thesis-section">
        <button class="collapsible-header" @click="noteOpen = !noteOpen">
          <span class="collapsible-header__title">碩論筆記</span>
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

      <!-- ── Kanban Board ── -->
      <section class="thesis-section">
        <div class="kanban-header">
          <h2 class="section-title">論文想法白板</h2>
          <button class="add-idea-btn" @click="showAddModal = true">＋ 新增想法</button>
        </div>
        <div class="kanban">
          <div v-for="col in kanbanCols" :key="col.status" class="kanban-col">
            <div class="kanban-col__header" :class="`kanban-col__header--${col.status}`">
              <span class="kanban-col__title">{{ col.label }}</span>
              <span class="kanban-col__count">{{ ideasByStatus(col.status).length }}</span>
            </div>
            <div class="kanban-col__body">
              <div v-if="!ideasByStatus(col.status).length" class="kanban-empty">尚無想法</div>
              <div
                v-for="idea in ideasByStatus(col.status)"
                :key="idea.id"
                class="kanban-card"
              >
                <div class="kanban-card__top">
                  <h4 class="kanban-card__title">{{ idea.title }}</h4>
                  <button class="kanban-card__del" @click="deleteIdea(idea.id)">×</button>
                </div>
                <p class="kanban-card__content">{{ idea.content }}</p>
                <p class="kanban-card__date">{{ idea.createdAt }}</p>
                <div class="kanban-card__actions">
                  <button
                    v-if="idea.status !== 'approved'"
                    class="kanban-card__btn kanban-card__btn--approve"
                    @click="changeStatus(idea.id, 'approved')"
                  >核准</button>
                  <button
                    v-if="idea.status !== 'rejected'"
                    class="kanban-card__btn kanban-card__btn--reject"
                    @click="changeStatus(idea.id, 'rejected')"
                  >拒絕</button>
                  <button
                    v-if="idea.status !== 'pending'"
                    class="kanban-card__btn kanban-card__btn--pending"
                    @click="changeStatus(idea.id, 'pending')"
                  >待審</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Reference Papers Table ── -->
      <section class="thesis-section">
        <div class="papers-header">
          <h2 class="section-title">文獻清單</h2>
          <div class="papers-filters">
            <input v-model="paperKeyword" class="filter-input" type="text" placeholder="搜尋標題…" @keyup.enter="fetchPapers" />
            <button class="filter-btn" @click="fetchPapers">搜尋</button>
          </div>
        </div>
        <div class="papers-table-wrap">
          <table class="papers-table">
            <thead>
              <tr>
                <th>主題</th>
                <th>論文名稱</th>
                <th>期刊</th>
                <th>作者</th>
                <th class="text-right">年份</th>
                <th>研究目的</th>
                <th>主要貢獻</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in papers" :key="p.id" class="paper-row">
                <td class="paper-cell">
                  <span class="topic-badge">{{ p.topic }}</span>
                </td>
                <td class="paper-cell paper-cell--name">{{ p.name }}</td>
                <td class="paper-cell paper-cell--journal">{{ p.journal }}</td>
                <td class="paper-cell">{{ p.authors }}</td>
                <td class="paper-cell text-right">{{ p.year }}</td>
                <td class="paper-cell paper-cell--long">{{ p.purpose }}</td>
                <td class="paper-cell paper-cell--long">{{ p.contribution }}</td>
              </tr>
              <tr v-if="!papers.length">
                <td colspan="7" class="paper-cell paper-cell--empty">沒有符合的文獻</td>
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
          <h3 class="modal__title">新增論文想法</h3>
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
import { ref, onMounted } from 'vue'
import {
  getThesisNote, saveThesisNote,
  getThesisIdeas, addThesisIdea, updateIdeaStatus, deleteThesisIdea,
  getThesisPapers,
} from '@/api/thesis'
import type { ThesisNote, ThesisIdea, ThesisPaper, IdeaStatus } from '@/types/thesis'

// ── Notes ──
const note = ref<ThesisNote>({ content: '', updatedAt: '' })
const noteOpen = ref(true)
const noteEditing = ref(false)
const editContent = ref('')

function startEdit() { editContent.value = note.value.content; noteEditing.value = true }
function cancelEdit() { noteEditing.value = false }
async function saveEdit() {
  await saveThesisNote(editContent.value)
  note.value.content = editContent.value
  note.value.updatedAt = new Date().toLocaleDateString('zh-TW')
  noteEditing.value = false
}

// ── Kanban ──
const ideas = ref<ThesisIdea[]>([])
const kanbanCols: { status: IdeaStatus; label: string }[] = [
  { status: 'pending', label: '待審核' },
  { status: 'rejected', label: '已拒絕' },
  { status: 'approved', label: '已核准' },
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

const showAddModal = ref(false)
const newIdea = ref({ title: '', content: '', status: 'pending' as IdeaStatus, createdAt: '' })

async function submitIdea() {
  if (!newIdea.value.title.trim()) return
  const today = new Date().toISOString().slice(0, 10)
  const created = await addThesisIdea({ ...newIdea.value, createdAt: today })
  ideas.value.push(created)
  newIdea.value = { title: '', content: '', status: 'pending', createdAt: '' }
  showAddModal.value = false
}

// ── Papers ──
const papers = ref<ThesisPaper[]>([])
const paperKeyword = ref('')

async function fetchPapers() {
  papers.value = await getThesisPapers('', '', paperKeyword.value)
}

onMounted(async () => {
  note.value = await getThesisNote()
  ideas.value = await getThesisIdeas()
  papers.value = await getThesisPapers()
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

.collapsible-header__title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.collapsible-header__arrow {
  font-size: 14px;
  color: var(--color-ink-2);
  transition: transform 0.2s;
}

.collapsible-header__arrow--open { transform: rotate(180deg); }

/* Note */
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
  width: 100%;
  padding: var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  resize: vertical;
  outline: none;
}
.note-edit__textarea:focus { border-color: var(--color-primary); }
.note-edit__actions { display: flex; gap: var(--space-2); justify-content: flex-end; }

.note-btn {
  padding: var(--space-2) var(--space-4);
  background: var(--color-ink-1);
  color: var(--color-white);
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  cursor: pointer;
  transition: opacity 0.2s;
  align-self: flex-start;
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
  padding: var(--space-2) var(--space-4);
  background: var(--color-ink-1);
  color: var(--color-white);
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.add-idea-btn:hover { opacity: 0.8; }

.kanban {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

.kanban-col {
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.kanban-col__header {
  padding: var(--space-3) var(--space-4);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.kanban-col__header--pending  { background: var(--color-primary-bg); border-bottom: 2px solid var(--color-primary); }
.kanban-col__header--rejected { background: #fef2f2; border-bottom: 2px solid #dc2626; }
.kanban-col__header--approved { background: #f0fdf4; border-bottom: 2px solid #16a34a; }

.kanban-col__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); }
.kanban-col__count {
  width: 22px; height: 22px; display: flex; align-items: center; justify-content: center;
  background: var(--color-ink-1); color: #fff; border-radius: 50%; font-size: 11px; font-weight: 700;
}

.kanban-col__body { padding: var(--space-3); display: flex; flex-direction: column; gap: var(--space-3); min-height: 120px; }

.kanban-empty { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-4); text-align: center; padding: var(--space-4) 0; }

.kanban-card {
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  padding: var(--space-3);
  background: var(--color-white);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.kanban-card__top { display: flex; align-items: flex-start; justify-content: space-between; }
.kanban-card__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); }
.kanban-card__del { background: none; border: none; font-size: 16px; color: var(--color-ink-4); cursor: pointer; line-height: 1; }
.kanban-card__del:hover { color: #dc2626; }
.kanban-card__content { font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-2); line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.kanban-card__date { font-size: 11px; color: var(--color-ink-4); }
.kanban-card__actions { display: flex; gap: var(--space-1); flex-wrap: wrap; }

.kanban-card__btn {
  padding: 2px 8px;
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.kanban-card__btn:hover { opacity: 0.8; }
.kanban-card__btn--approve { background: #16a34a; color: #fff; }
.kanban-card__btn--reject  { background: #dc2626; color: #fff; }
.kanban-card__btn--pending { background: var(--color-primary); color: var(--color-ink-1); }

/* ── Papers ── */
.papers-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.papers-filters { display: flex; gap: var(--space-2); }

.filter-input {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  outline: none;
  width: 200px;
  transition: border-color 0.2s;
}
.filter-input:focus { border-color: var(--color-primary); }

.filter-btn {
  padding: var(--space-2) var(--space-4);
  background: var(--color-ink-1);
  color: var(--color-white);
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.filter-btn:hover { opacity: 0.8; }

.papers-table-wrap { overflow-x: auto; }

.papers-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.papers-table th {
  padding: var(--space-3);
  background: var(--color-primary-bg);
  font-family: var(--font-cjk);
  font-weight: 700;
  color: var(--color-ink-1);
  border-bottom: 2px solid var(--color-primary);
  text-align: left;
  white-space: nowrap;
}

.paper-row:nth-child(even) { background: #fafafa; }
.paper-row:hover { background: var(--color-primary-bg); }

.paper-cell {
  padding: var(--space-3);
  font-family: var(--font-cjk);
  color: var(--color-ink-2);
  border-bottom: 1px solid var(--color-ink-4);
  vertical-align: top;
}

.paper-cell--name { font-weight: 600; color: var(--color-ink-1); max-width: 240px; }
.paper-cell--journal { max-width: 180px; color: var(--color-secondary); font-weight: 600; }
.paper-cell--long { max-width: 260px; line-height: 1.6; white-space: normal; }
.paper-cell--empty { text-align: center; color: var(--color-ink-4); padding: var(--space-6) 0; }

.text-right { text-align: right; }

.topic-badge {
  padding: 2px 8px;
  background: var(--color-primary-bg);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 700;
  color: var(--color-ink-1);
}

/* ── Add Idea Modal ── */
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: var(--color-white); border-radius: var(--radius-md); padding: var(--space-6); width: 480px; max-width: 90vw; position: relative; display: flex; flex-direction: column; gap: var(--space-4); }
.modal__close { position: absolute; top: var(--space-4); right: var(--space-4); font-size: 20px; background: none; border: none; cursor: pointer; color: var(--color-ink-3); }
.modal__title { font-family: var(--font-cjk); font-size: 18px; font-weight: 700; color: var(--color-ink-1); }

.modal__label {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}

.modal__input, .modal__textarea {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  outline: none;
  width: 100%;
  box-sizing: border-box;
  transition: border-color 0.2s;
}
.modal__input:focus, .modal__textarea:focus { border-color: var(--color-primary); }
.modal__textarea { resize: vertical; }

.modal__actions { display: flex; gap: var(--space-2); justify-content: flex-end; }

.modal__btn {
  padding: var(--space-2) var(--space-5);
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.modal__btn:hover { opacity: 0.82; }
.modal__btn--cancel { background: var(--color-ink-4); color: var(--color-ink-1); }
.modal__btn--add    { background: var(--color-primary); color: var(--color-ink-1); }

@media (max-width: 767px) {
  .kanban { grid-template-columns: 1fr; }
  .metric-cards { grid-template-columns: 1fr 1fr; }
}
</style>
