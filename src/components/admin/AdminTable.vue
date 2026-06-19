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
            <th v-for="col in columns" :key="col">{{ col }}</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!rows.length">
            <td :colspan="columns.length + 1" class="crud-empty">尚無資料</td>
          </tr>
          <tr v-for="(row, i) in rows" :key="ids[i]" class="crud-row">
            <td v-for="(cell, j) in row" :key="j" class="crud-cell">{{ cell }}</td>
            <td class="crud-cell crud-cell--actions">
              <button class="crud-btn crud-btn--edit" @click="$emit('edit', ids[i])">編輯</button>
              <button class="crud-btn crud-btn--del"  @click="$emit('delete', ids[i])">刪除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title:   string
  columns: string[]
  rows:    string[][]
  ids:     number[]
}>()

defineEmits<{
  add:    []
  edit:   [id: number]
  delete: [id: number]
}>()
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

.crud-row:nth-child(even) { background: #fafafa; }
.crud-row:hover { background: var(--color-primary-bg); }

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
