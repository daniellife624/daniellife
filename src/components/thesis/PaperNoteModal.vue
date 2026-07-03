<template>
  <Teleport to="body">
    <div v-if="paper" class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal">
        <button class="modal__close" @click="$emit('close')">×</button>
        <h3 class="modal__title">筆記：{{ paper.name }}</h3>

        <div v-if="paper.notes" class="note-content" v-html="paper.notes"></div>
        <p v-else class="note-empty">
          尚無筆記內容。請先在
          <a v-if="paper.notionUrl" :href="paper.notionUrl" target="_blank" rel="noopener">Notion 頁面</a>
          <span v-else>Notion</span>
          寫下重點，再回 Admin 面板按「同步 Notion 筆記」。
        </p>

        <a v-if="paper.notionUrl" :href="paper.notionUrl" target="_blank" rel="noopener" class="notion-link">
          在 Notion 開啟並編輯 ↗
        </a>

        <div class="modal__actions">
          <button class="modal__btn modal__btn--cancel" @click="$emit('close')">關閉</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import type { ThesisPaper } from '@/types/thesis'

defineProps<{ paper: ThesisPaper | null }>()
defineEmits<{ close: [] }>()
</script>

<style scoped>
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: var(--color-white); border-radius: var(--radius-md); padding: var(--space-6); width: 640px; max-width: 92vw; max-height: 88vh; overflow-y: auto; position: relative; display: flex; flex-direction: column; gap: var(--space-3); }
.modal__close { position: absolute; top: var(--space-4); right: var(--space-4); font-size: 20px; background: none; border: none; cursor: pointer; color: var(--color-ink-3); }
.modal__title { font-family: var(--font-cjk); font-size: 18px; font-weight: 700; color: var(--color-ink-1); padding-right: var(--space-6); }

.note-content {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-1);
  line-height: 1.8;
}
.note-content :deep(p) { margin: 0 0 var(--space-2); }
.note-content :deep(h3),
.note-content :deep(h4),
.note-content :deep(h5) { margin: var(--space-3) 0 var(--space-2); color: var(--color-ink-1); }
.note-content :deep(ul),
.note-content :deep(ol) { margin: 0 0 var(--space-2); padding-left: 1.4em; }
.note-content :deep(blockquote) { margin: var(--space-2) 0; padding: var(--space-2) var(--space-3); border-left: 3px solid var(--color-primary); background: var(--color-primary-bg); color: var(--color-ink-2); }
.note-content :deep(pre) { background: #f5f5f5; padding: var(--space-3); border-radius: var(--radius-sm); overflow-x: auto; }
.note-content :deep(img) { max-width: 100%; border-radius: var(--radius-sm); }
.note-content :deep(hr) { border: none; border-top: 1px solid var(--color-ink-4); margin: var(--space-3) 0; }

.note-empty { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-3); line-height: 1.7; }
.note-empty a { color: var(--color-secondary); }

.notion-link { align-self: flex-start; font-family: var(--font-cjk); font-size: 13px; color: var(--color-secondary); font-weight: 600; }
.notion-link:hover { text-decoration: underline; }

.modal__actions { display: flex; gap: var(--space-2); justify-content: flex-end; }
.modal__btn { padding: var(--space-2) var(--space-5); border: none; border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 14px; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
.modal__btn:hover { opacity: 0.82; }
.modal__btn--cancel { background: var(--color-ink-4); color: var(--color-ink-1); }
</style>
