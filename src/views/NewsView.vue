<template>
  <div class="news">
    <div class="news__inner">
      <NewsList />
      <ChatPanel />
    </div>
  </div>
</template>

<script setup lang="ts">
import NewsList from '@/components/news/NewsList.vue'
import ChatPanel from '@/components/news/ChatPanel.vue'
</script>

<style scoped>
.news {
  padding: var(--space-6) var(--space-6) var(--space-8);
  background: var(--color-white);
  min-height: calc(100vh - 64px);
}

.news__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  display: flex;
  gap: var(--space-6);
  align-items: flex-start;
}

@media (max-width: 960px) { .news__inner { flex-direction: column; } }
</style>
