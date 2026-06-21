<template>
  <aside class="admin__sidebar">
    <p class="admin__sidebar-title">資料管理</p>
    <button
      v-for="sec in sections"
      :key="sec.key"
      class="admin__sidebar-item"
      :class="{ 'admin__sidebar-item--active': currentSection === sec.key }"
      @click="$emit('select', sec.key)"
    >{{ sec.label }}</button>
    <div class="admin__sidebar-divider"></div>
    <button class="admin__logout" @click="$emit('logout')">登出</button>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  sections: { key: string; label: string }[]
  currentSection: string
}>()
defineEmits<{
  select: [key: string]
  logout: []
}>()
</script>

<style scoped>
.admin__sidebar {
  flex-shrink: 0;
  width: 200px;
  background: var(--color-ink-1);
  padding: var(--space-6) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  position: sticky;
  top: var(--navbar-height);
  height: calc(100vh - var(--navbar-height));
  overflow-y: auto;
}

.admin__sidebar-title {
  font-family: var(--font-cjk);
  font-size: 11px;
  font-weight: 700;
  color: var(--color-ink-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: var(--space-2) var(--space-3);
  margin-bottom: var(--space-2);
}

.admin__sidebar-item {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  background: none;
  border: none;
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-3);
  cursor: pointer;
  text-align: left;
  transition: background 0.15s, color 0.15s;
}
.admin__sidebar-item:hover { background: rgba(255,255,255,0.06); color: #fff; }
.admin__sidebar-item--active { background: var(--color-primary); color: var(--color-ink-1); font-weight: 700; }

.admin__sidebar-divider {
  height: 1px;
  background: rgba(255,255,255,0.1);
  margin: var(--space-4) 0;
}

.admin__logout {
  padding: var(--space-2) var(--space-3);
  background: none;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
  cursor: pointer;
  text-align: left;
  transition: border-color 0.2s, color 0.2s;
  margin-top: auto;
}
.admin__logout:hover { border-color: #dc2626; color: #dc2626; }
</style>
