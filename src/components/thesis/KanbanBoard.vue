<template>
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
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getThesisIdeas, addThesisIdea, updateIdeaStatus, deleteThesisIdea } from '@/api/thesis'
import type { ThesisIdea, IdeaStatus } from '@/types/thesis'

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

const showAddModal = ref(false)
const newIdea = ref({ title: '', content: '', status: 'pending' as IdeaStatus, createdAt: '' })

async function submitIdea() {
  if (!newIdea.value.title.trim()) return
  const created = await addThesisIdea({ ...newIdea.value, createdAt: new Date().toISOString().slice(0, 10) })
  ideas.value.push(created)
  newIdea.value = { title: '', content: '', status: 'pending', createdAt: '' }
  showAddModal.value = false
}

onMounted(async () => { ideas.value = await getThesisIdeas() })
</script>

<style scoped>
.thesis-section { display: flex; flex-direction: column; }

.section-title { font-family: var(--font-cjk); font-size: 20px; font-weight: 700; color: var(--color-ink-1); }

.kanban-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-4); }

.add-idea-btn {
  padding: var(--space-2) var(--space-4); background: var(--color-ink-1); color: var(--color-white);
  border: none; border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 13px;
  font-weight: 600; cursor: pointer; transition: opacity 0.2s;
}
.add-idea-btn:hover { opacity: 0.8; }

.kanban { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.kanban-col { border: 1px solid var(--color-ink-4); border-radius: var(--radius-md); overflow: hidden; }

.kanban-col__header { padding: var(--space-3) var(--space-4); display: flex; align-items: center; justify-content: space-between; }
.kanban-col__header--pending  { background: var(--color-primary-bg); border-bottom: 2px solid var(--color-primary); }
.kanban-col__header--rejected { background: #fef2f2; border-bottom: 2px solid #dc2626; }
.kanban-col__header--approved { background: #f0fdf4; border-bottom: 2px solid #16a34a; }

.kanban-col__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); }
.kanban-col__count { width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; background: var(--color-ink-1); color: #fff; border-radius: 50%; font-size: 11px; font-weight: 700; }

.kanban-col__body { padding: var(--space-3); display: flex; flex-direction: column; gap: var(--space-3); min-height: 140px; transition: background 0.15s; }
.kanban-col__body--over { background: rgba(232, 193, 58, 0.08); }

.kanban-empty { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-4); text-align: center; padding: var(--space-4) 0; border: 2px dashed var(--color-ink-4); border-radius: var(--radius-sm); pointer-events: none; }

.sticky-card { background: #fffde7; border-radius: var(--radius-sm); padding: var(--space-3); display: flex; flex-direction: column; gap: var(--space-2); box-shadow: 0 2px 6px rgba(0,0,0,0.08); cursor: grab; transition: opacity 0.2s, box-shadow 0.2s; user-select: none; }
.sticky-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.13); }
.sticky-card--dragging { opacity: 0.4; cursor: grabbing; }

.sticky-card__top { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--space-2); }
.sticky-card__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); line-height: 1.4; }
.sticky-card__del { background: none; border: none; font-size: 16px; color: var(--color-ink-4); cursor: pointer; flex-shrink: 0; line-height: 1; padding: 0; }
.sticky-card__del:hover { color: #dc2626; }
.sticky-card__content { font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-2); line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }

.sticky-card__date { font-size: 11px; color: var(--color-ink-4); }

.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: var(--color-white); border-radius: var(--radius-md); padding: var(--space-6); width: 480px; max-width: 90vw; position: relative; display: flex; flex-direction: column; gap: var(--space-4); }
.modal__close { position: absolute; top: var(--space-4); right: var(--space-4); font-size: 20px; background: none; border: none; cursor: pointer; color: var(--color-ink-3); }
.modal__title { font-family: var(--font-cjk); font-size: 18px; font-weight: 700; color: var(--color-ink-1); }
.modal__label { display: flex; flex-direction: column; gap: var(--space-1); font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); }
.modal__input, .modal__textarea { padding: var(--space-2) var(--space-3); border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 14px; outline: none; width: 100%; box-sizing: border-box; transition: border-color 0.2s; }
.modal__input:focus, .modal__textarea:focus { border-color: var(--color-primary); }
.modal__textarea { resize: vertical; }
.modal__actions { display: flex; gap: var(--space-2); justify-content: flex-end; }
.modal__btn { padding: var(--space-2) var(--space-5); border: none; border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 14px; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
.modal__btn:hover { opacity: 0.82; }
.modal__btn--cancel { background: var(--color-ink-4); color: var(--color-ink-1); }
.modal__btn--add    { background: var(--color-primary); color: var(--color-ink-1); }

@media (max-width: 767px) { .kanban { grid-template-columns: 1fr; } }
</style>
