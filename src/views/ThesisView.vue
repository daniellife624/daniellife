<template>
  <div class="thesis">
    <div class="thesis__inner">
      <ThesisNotePanel />
      <KanbanBoard />
      <PapersTable />
    </div>
  </div>
</template>

<script setup lang="ts">
import ThesisNotePanel from '@/components/thesis/ThesisNotePanel.vue'
import KanbanBoard from '@/components/thesis/KanbanBoard.vue'
import PapersTable from '@/components/thesis/PapersTable.vue'
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
</style>
