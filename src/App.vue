<template>
  <AppNavbar />
  <main>
    <RouterView />
  </main>
  <AppFooter />

  <Transition name="fade-up">
    <button
      v-if="showTop"
      class="back-to-top"
      @click="scrollTop"
      aria-label="回到頂端"
    >
      ↑
    </button>
  </Transition>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const showTop = ref(false)

function onScroll() {
  showTop.value = window.scrollY > 300
}

function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
main {
  min-height: calc(100vh - var(--navbar-height));
  padding-top: var(--navbar-height);
}

.back-to-top {
  position: fixed;
  bottom: 28px;
  right: 28px;
  z-index: 900;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid var(--color-primary);
  background: #fff;
  color: var(--color-ink-1);
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transition: background 0.2s, transform 0.2s;
  line-height: 1;
}

.back-to-top:hover {
  background: var(--color-primary);
  transform: translateY(-2px);
}

.fade-up-enter-active,
.fade-up-leave-active {
  transition: opacity 0.28s ease, transform 0.28s ease;
}
.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
