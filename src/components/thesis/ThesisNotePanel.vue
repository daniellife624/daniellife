<template>
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getThesisNote, saveThesisNote } from '@/api/thesis'
import type { ThesisNote } from '@/types/thesis'

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

onMounted(async () => { note.value = await getThesisNote() })
</script>

<style scoped>
.thesis-section { display: flex; flex-direction: column; }

.collapsible-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  background: var(--color-primary-bg);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  cursor: pointer; font-family: var(--font-cjk);
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
</style>
