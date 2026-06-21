<template>
  <a
    :href="item.url || '#'"
    :target="item.url ? '_blank' : '_self'"
    rel="noopener"
    class="news-card"
  >
    <h3 class="news-card__title">{{ item.title }}</h3>
    <p class="news-card__summary">{{ item.summary }}</p>
    <div class="news-card__footer">
      <time class="news-card__time">{{ item.publishedAt }}</time>
      <span class="news-card__source">{{ item.source }}</span>
    </div>
  </a>
</template>

<script setup lang="ts">
import type { NewsItem } from '@/types/market'
defineProps<{ item: NewsItem }>()
</script>

<style scoped>
.news-card {
  display: block;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
  text-decoration: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.news-card:hover { border-color: var(--color-primary); box-shadow: 0 2px 8px rgba(0,0,0,0.05); }

.news-card__title { font-family: var(--font-cjk); font-size: 15px; font-weight: 700; color: var(--color-ink-1); line-height: 1.5; margin-bottom: var(--space-2); }
.news-card__summary { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); line-height: 1.7; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: var(--space-3); }

.news-card__footer { display: flex; align-items: center; justify-content: space-between; }
.news-card__time { font-size: 12px; color: var(--color-ink-3); font-family: var(--font-body); }
.news-card__source { font-size: 11px; font-weight: 600; background: var(--color-secondary); color: var(--color-white); padding: 2px 8px; border-radius: 3px; letter-spacing: 0.02em; }
</style>
