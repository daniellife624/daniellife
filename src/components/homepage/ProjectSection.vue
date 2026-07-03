<template>
  <section class="project">
    <div class="project__inner">
      <div class="project__header">
        <h2 class="section-title">專案經驗</h2>
        <span class="section-tag">財會 x 程式 x UIUX</span>
      </div>

      <div class="project__filters">
        <div class="project__select-wrap">
          <select v-model="filterType" class="project__select">
            <option value="">專案類型：</option>
            <option value="code">程式</option>
            <option value="uiux">UIUX</option>
            <option value="finance">財會</option>
          </select>
          <span class="project__chevron">∨</span>
        </div>
        <div class="project__select-wrap">
          <select v-model="filterKeyword" class="project__select">
            <option value="">專案關鍵字：</option>
            <option value="Vue.js">Vue.js</option>
            <option value="Python">Python</option>
            <option value="Figma">Figma</option>
          </select>
          <span class="project__chevron">∨</span>
        </div>
        <div class="project__select-wrap">
          <select v-model="filterMembers" class="project__select">
            <option value="">專案參與人數：</option>
            <option value="small">1–5 人</option>
            <option value="mid">6–10 人</option>
            <option value="large">10 人以上</option>
          </select>
          <span class="project__chevron">∨</span>
        </div>
      </div>

      <div class="project__grid">
        <article
          v-for="proj in filteredProjects"
          :key="proj.id"
          class="project-card"
        >
          <div class="project-card__header">
            <h3 class="project-card__name">{{ proj.name }}</h3>
            <div class="project-card__links">
              <span class="project-card__link-label">專案連結</span>
              <a v-if="proj.githubUrl" :href="proj.githubUrl" target="_blank" class="project-card__link-icon" title="GitHub">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.2 11.39.6.11.82-.26.82-.58v-2.18c-3.34.73-4.04-1.6-4.04-1.6-.54-1.38-1.33-1.75-1.33-1.75-1.09-.74.08-.73.08-.73 1.2.08 1.84 1.24 1.84 1.24 1.07 1.83 2.8 1.3 3.49 1 .1-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.28-1.55 3.29-1.23 3.29-1.23.66 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.63-5.48 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.21.7.82.58C20.56 21.8 24 17.3 24 12c0-6.63-5.37-12-12-12z"/></svg>
              </a>
              <a v-if="proj.youtubeUrl" :href="proj.youtubeUrl" target="_blank" class="project-card__link-icon" title="YouTube">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3.02 3.02 0 0 0-2.12-2.14C19.54 3.6 12 3.6 12 3.6s-7.54 0-9.38.47A3.02 3.02 0 0 0 .5 6.2C0 8.05 0 12 0 12s0 3.95.5 5.8a3.02 3.02 0 0 0 2.12 2.14C4.46 20.4 12 20.4 12 20.4s7.54 0 9.38-.46a3.02 3.02 0 0 0 2.12-2.14C24 15.95 24 12 24 12s0-3.95-.5-5.8zM9.6 15.6V8.4l6.27 3.6-6.27 3.6z"/></svg>
              </a>
              <a v-if="proj.otherUrl" :href="proj.otherUrl" target="_blank" class="project-card__link-icon" title="其他連結">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
              </a>
            </div>
            <div class="project-card__badges">
              <span
                v-for="t in typesOf(proj)"
                :key="t"
                class="project-card__badge"
                :class="`project-card__badge--${t}`"
              >{{ typeLabel[t] }}</span>
            </div>
          </div>

          <div class="project-card__core">
            <span class="project-card__core-label">專案核心（20字）</span>
            <span class="project-card__core-text">{{ proj.core }}</span>
          </div>

          <table class="project-card__table">
            <tr>
              <td class="project-card__td-key">{{ proj.techLabel }}</td>
              <td class="project-card__td-val">{{ proj.tech }}</td>
            </tr>
            <tr v-if="proj.responsibility">
              <td class="project-card__td-key">主要職責</td>
              <td class="project-card__td-val">{{ proj.responsibility }}</td>
            </tr>
            <tr>
              <td class="project-card__td-key">參與專案人數</td>
              <td class="project-card__td-val">{{ proj.members }}</td>
            </tr>
            <tr>
              <td class="project-card__td-key">專案期間</td>
              <td class="project-card__td-val">{{ proj.period }}</td>
            </tr>
          </table>

          <div class="project-card__star">
            <div v-for="s in proj.star" :key="s.label" class="project-card__star-item">
              <span class="project-card__star-badge" :class="`project-card__star-badge--${typesOf(proj)[0] ?? 'code'}`">{{ s.label }}</span>
              <p class="project-card__star-text">{{ s.text }}</p>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getProjects } from '@/api/homepage'
import type { Project } from '@/types/homepage'

const filterType = ref('')
const filterKeyword = ref('')
const filterMembers = ref('')
const allProjects = ref<Project[]>([])

const typeLabel: Record<string, string> = { code: '程式', uiux: 'UIUX', finance: '財會' }

function typesOf(p: Project): string[] {
  return p.type.split(',').map((t) => t.trim()).filter(Boolean)
}

onMounted(async () => {
  allProjects.value = await getProjects()
})

const filteredProjects = computed(() => {
  return allProjects.value.filter((p) => {
    if (filterType.value && !typesOf(p).includes(filterType.value)) return false
    if (filterKeyword.value && !p.tech.includes(filterKeyword.value)) return false
    if (filterMembers.value === 'small' && p.members > 5) return false
    if (filterMembers.value === 'mid' && (p.members < 6 || p.members > 10)) return false
    if (filterMembers.value === 'large' && p.members <= 10) return false
    return true
  })
})
</script>

<style scoped>
.project {
  padding: var(--space-8) var(--space-6);
  background-color: var(--color-white);
  border-top: 1px solid var(--color-ink-4);
}

.project__inner {
  max-width: var(--container-max);
  margin: 0 auto;
}

.project__header {
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}

.section-title {
  font-family: var(--font-cjk);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.section-tag {
  font-size: 13px;
  color: var(--color-ink-3);
}

.project__filters {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.project__select-wrap {
  flex: 1;
  position: relative;
}

.project__select {
  width: 100%;
  padding: var(--space-3) var(--space-5) var(--space-3) var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-2);
  background: var(--color-white);
  cursor: pointer;
  appearance: none;
}

.project__chevron {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: var(--color-ink-3);
  pointer-events: none;
}

.project__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
}

.project-card {
  background: var(--color-white);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* ── Card Header ── */
.project-card__header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.project-card__name {
  font-family: var(--font-cjk);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-ink-1);
  flex: 1;
  min-width: 0;
}

.project-card__links {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-shrink: 0;
}

.project-card__link-label {
  font-size: 11px;
  color: var(--color-ink-3);
}

.project-card__link-icon {
  width: 26px;
  height: 26px;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-ink-2);
  transition: color 0.2s, border-color 0.2s;
}

.project-card__link-icon:hover {
  color: var(--color-ink-1);
  border-color: var(--color-ink-2);
}

.project-card__badges {
  display: flex;
  gap: var(--space-1);
  flex-shrink: 0;
}

.project-card__badge {
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

.project-card__badge--code    { background: var(--color-secondary); color: #fff; }
.project-card__badge--uiux    { background: var(--color-primary); color: var(--color-ink-1); }
.project-card__badge--finance { background: var(--color-tertiary); color: #fff; }

/* ── Core ── */
.project-card__core {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.project-card__core-label {
  font-size: 11px;
  color: var(--color-ink-3);
}

.project-card__core-text {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-1);
  line-height: 1.6;
}

/* ── Table ── */
.project-card__table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.project-card__td-key {
  color: var(--color-ink-3);
  padding: 3px 0;
  width: 40%;
  vertical-align: top;
  white-space: nowrap;
}

.project-card__td-val {
  color: var(--color-ink-1);
  font-weight: 600;
  padding: 3px 0;
  vertical-align: top;
}

/* ── STAR ── */
.project-card__star {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.project-card__star-item {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}

.project-card__star-badge {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  flex-shrink: 0;
}

.project-card__star-badge--code    { background: var(--color-secondary); color: #fff; }
.project-card__star-badge--uiux    { background: var(--color-primary); color: var(--color-ink-1); }
.project-card__star-badge--finance { background: var(--color-tertiary); color: #fff; }

.project-card__star-text {
  font-size: 12px;
  color: var(--color-ink-2);
  line-height: 1.6;
}

@media (max-width: 767px) {
  .project__grid    { grid-template-columns: 1fr; }
  .project__filters { flex-direction: column; }
}
</style>
