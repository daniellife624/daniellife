<template>
  <Teleport to="body">
    <div v-if="paper" class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal">
        <button class="modal__close" @click="$emit('close')">×</button>
        <h3 class="modal__title">筆記：{{ paper.name }}</h3>

        <div class="editor-toolbar">
          <button type="button" class="toolbar-btn" title="粗體" @mousedown.prevent="exec('bold')"><b>B</b></button>
          <button type="button" class="toolbar-btn" title="項目符號" @mousedown.prevent="exec('insertUnorderedList')">• 清單</button>
          <span v-if="pendingCount > 0" class="toolbar-status">圖片上傳中…</span>
        </div>

        <div
          ref="editorRef"
          class="editor"
          contenteditable="true"
          data-placeholder="輸入重點，或直接貼上圖片…"
          @paste="onPaste"
        ></div>

        <p v-if="uploadError" class="modal__error">{{ uploadError }}</p>
        <div class="modal__actions">
          <button class="modal__btn modal__btn--cancel" @click="$emit('close')">取消</button>
          <button class="modal__btn modal__btn--save" :disabled="saving || pendingCount > 0" @click="save">
            {{ saving ? '儲存中…' : '儲存' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { updatePaperNotes, uploadPaperNoteImage } from '@/api/thesis'
import { mediaUrl } from '@/api/client'
import type { ThesisPaper } from '@/types/thesis'

const props = defineProps<{ paper: ThesisPaper | null }>()
const emit = defineEmits<{ close: []; saved: [paper: ThesisPaper] }>()

const editorRef    = ref<HTMLDivElement | null>(null)
const saving        = ref(false)
const pendingCount  = ref(0)
const uploadError   = ref('')

watch(() => props.paper, (p) => {
  uploadError.value = ''
  if (p && editorRef.value) {
    editorRef.value.innerHTML = p.notes ?? ''
  }
})

function exec(command: string) {
  editorRef.value?.focus()
  document.execCommand(command)
}

async function onPaste(e: ClipboardEvent) {
  const items = e.clipboardData?.items
  if (!items || !props.paper) return
  for (const item of items) {
    if (item.type.startsWith('image/')) {
      e.preventDefault()
      const file = item.getAsFile()
      if (file) await insertImage(file, props.paper.id)
      return
    }
  }
}

async function insertImage(file: File, paperId: number) {
  const tempId = `pending-${Date.now()}-${Math.random().toString(36).slice(2)}`
  const reader = new FileReader()
  reader.onload = async (ev) => {
    const dataUrl = ev.target?.result as string
    editorRef.value?.focus()
    document.execCommand('insertHTML', false, `<img src="${dataUrl}" data-pending="${tempId}" style="max-width:100%;border-radius:4px;display:block;margin:8px 0;" />`)

    pendingCount.value++
    try {
      const { url } = await uploadPaperNoteImage(paperId, file)
      const img = editorRef.value?.querySelector<HTMLImageElement>(`img[data-pending="${tempId}"]`)
      if (img) {
        img.setAttribute('src', mediaUrl(url))
        img.removeAttribute('data-pending')
      }
    } catch {
      uploadError.value = '圖片上傳失敗，已移除該張圖片'
      editorRef.value?.querySelector(`img[data-pending="${tempId}"]`)?.remove()
    } finally {
      pendingCount.value--
    }
  }
  reader.readAsDataURL(file)
}

async function save() {
  if (!props.paper || !editorRef.value) return
  saving.value = true
  uploadError.value = ''
  try {
    const updated = await updatePaperNotes(props.paper.id, editorRef.value.innerHTML)
    emit('saved', updated)
    emit('close')
  } catch {
    uploadError.value = '儲存失敗，請再試一次'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: var(--color-white); border-radius: var(--radius-md); padding: var(--space-6); width: 640px; max-width: 92vw; max-height: 88vh; overflow-y: auto; position: relative; display: flex; flex-direction: column; gap: var(--space-3); }
.modal__close { position: absolute; top: var(--space-4); right: var(--space-4); font-size: 20px; background: none; border: none; cursor: pointer; color: var(--color-ink-3); }
.modal__title { font-family: var(--font-cjk); font-size: 18px; font-weight: 700; color: var(--color-ink-1); padding-right: var(--space-6); }

.editor-toolbar { display: flex; align-items: center; gap: var(--space-2); }
.toolbar-btn { padding: var(--space-1) var(--space-3); border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm); background: var(--color-white); font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); cursor: pointer; transition: border-color 0.15s, color 0.15s; }
.toolbar-btn:hover { border-color: var(--color-ink-1); color: var(--color-ink-1); }
.toolbar-status { font-size: 12px; color: var(--color-ink-3); font-family: var(--font-cjk); }

.editor {
  min-height: 240px;
  max-height: 50vh;
  overflow-y: auto;
  padding: var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-1);
  line-height: 1.7;
  outline: none;
}
.editor:focus { border-color: var(--color-primary); }
.editor:empty::before { content: attr(data-placeholder); color: var(--color-ink-4); }

.modal__error { font-family: var(--font-cjk); font-size: 13px; color: #dc2626; background: #fef2f2; padding: var(--space-2) var(--space-3); border-radius: var(--radius-sm); }

.modal__actions { display: flex; gap: var(--space-2); justify-content: flex-end; }
.modal__btn { padding: var(--space-2) var(--space-5); border: none; border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 14px; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
.modal__btn:disabled { opacity: 0.6; cursor: not-allowed; }
.modal__btn:not(:disabled):hover { opacity: 0.82; }
.modal__btn--cancel { background: var(--color-ink-4); color: var(--color-ink-1); }
.modal__btn--save   { background: var(--color-primary); color: var(--color-ink-1); }
</style>
