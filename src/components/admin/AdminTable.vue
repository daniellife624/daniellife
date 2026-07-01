<template>
  <div class="crud-section">
    <div class="crud-section__header">
      <h2 class="crud-section__title">{{ title }}</h2>
      <button class="crud-btn crud-btn--add" @click="$emit('add')">＋ 新增</button>
    </div>
    <div class="crud-table-wrap">
      <table class="crud-table">
        <thead>
          <tr>
            <th v-if="draggable" class="crud-th--drag"></th>
            <th v-for="col in columns" :key="col">{{ col }}</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!rows.length">
            <td :colspan="columns.length + (draggable ? 2 : 1)" class="crud-empty">尚無資料</td>
          </tr>
          <tr
            v-for="(row, i) in rows"
            :key="ids[i]"
            class="crud-row"
            :class="{
              'crud-row--drag-over': draggable && dragOverIdx === i && draggingIdx !== i,
              'crud-row--dragging':  draggable && draggingIdx === i,
            }"
            :draggable="draggable || undefined"
            @dragstart="draggable ? onDragStart($event, i) : undefined"
            @dragover.prevent="draggable ? onDragOver(i) : undefined"
            @drop.prevent="draggable ? onDrop(i) : undefined"
            @dragend="draggable ? onDragEnd() : undefined"
          >
            <td v-if="draggable" class="crud-cell crud-cell--drag">
              <span class="drag-handle">⠿</span>
            </td>
            <td v-for="(cell, j) in row" :key="j" class="crud-cell">{{ cell }}</td>
            <td class="crud-cell crud-cell--actions">
              <button class="crud-btn crud-btn--edit" @click="$emit('edit', ids[i] ?? 0)">編輯</button>
              <button class="crud-btn crud-btn--del"  @click="$emit('delete', ids[i] ?? 0)">刪除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

withDefaults(defineProps<{
  title:     string
  columns:   string[]
  rows:      string[][]
  ids:       number[]
  draggable?: boolean
}>(), { draggable: false })

const emit = defineEmits<{
  add:     []
  edit:    [id: number]
  delete:  [id: number]
  reorder: [fromIndex: number, toIndex: number]
}>()

const draggingIdx = ref<number | null>(null)
const dragOverIdx = ref<number | null>(null)

function onDragStart(e: DragEvent, i: number) {
  draggingIdx.value = i
  if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move'
}

function onDragOver(i: number) {
  dragOverIdx.value = i
}

function onDrop(i: number) {
  if (draggingIdx.value !== null && draggingIdx.value !== i) {
    emit('reorder', draggingIdx.value, i)
  }
  draggingIdx.value = null
  dragOverIdx.value = null
}

function onDragEnd() {
  draggingIdx.value = null
  dragOverIdx.value = null
}
</script>

<style scoped>
.crud-section { display: flex; flex-direction: column; gap: var(--space-5); }

.crud-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.crud-section__title {
  font-family: var(--font-cjk);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.crud-table-wrap { overflow-x: auto; }

.crud-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  background: var(--color-white);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.crud-table th {
  padding: var(--space-3) var(--space-4);
  background: var(--color-primary-bg);
  font-family: var(--font-cjk);
  font-weight: 700;
  color: var(--color-ink-1);
  border-bottom: 2px solid var(--color-primary);
  text-align: left;
  white-space: nowrap;
}

.crud-th--drag { width: 32px; }

.crud-row:nth-child(even) { background: #fafafa; }
.crud-row:hover { background: var(--color-primary-bg); }
.crud-row--drag-over { border-top: 2px solid var(--color-primary); }
.crud-row--dragging { opacity: 0.35; }

.crud-cell {
  padding: var(--space-3) var(--space-4);
  font-family: var(--font-cjk);
  color: var(--color-ink-2);
  border-bottom: 1px solid var(--color-ink-4);
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.crud-cell--drag {
  width: 32px;
  text-align: center;
  max-width: 32px;
  cursor: grab;
  color: var(--color-ink-4);
}

.drag-handle {
  font-size: 16px;
  user-select: none;
  display: inline-block;
}

.crud-cell--actions {
  display: flex;
  gap: var(--space-2);
  align-items: center;
  max-width: none;
  white-space: nowrap;
}

.crud-empty {
  text-align: center;
  padding: var(--space-7) 0;
  color: var(--color-ink-4);
  font-family: var(--font-cjk);
  font-size: 14px;
}

.crud-btn {
  padding: var(--space-1) var(--space-3);
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  white-space: nowrap;
}
.crud-btn:hover { opacity: 0.8; }
.crud-btn--add  { background: var(--color-ink-1); color: #fff; padding: var(--space-2) var(--space-4); font-size: 13px; }
.crud-btn--edit { background: var(--color-primary); color: var(--color-ink-1); }
.crud-btn--del  { background: #fee2e2; color: #dc2626; }
</style>
