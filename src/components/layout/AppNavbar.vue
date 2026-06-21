<template>
  <header class="navbar">
    <div class="navbar__inner">
      <!-- Logo -->
      <RouterLink to="/" class="navbar__brand">
        <div class="navbar__logo">D</div>
        <span class="navbar__title">Daniellife 會計丹尼</span>
      </RouterLink>

      <!-- Desktop Nav -->
      <nav class="navbar__nav">
        <RouterLink
          v-for="item in visibleNavItems"
          :key="item.name"
          :to="item.path"
          class="navbar__link"
          active-class="navbar__link--active"
        >
          {{ item.label }}
        </RouterLink>
      </nav>

      <!-- Mobile Hamburger -->
      <button class="navbar__hamburger" @click="toggleMenu">
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
      </button>
    </div>

    <!-- Mobile Menu -->
    <nav v-if="menuOpen" class="navbar__mobile">
      <RouterLink
        v-for="item in visibleNavItems"
        :key="item.name"
        :to="item.path"
        class="navbar__mobile-link"
        active-class="navbar__link--active"
        @click="menuOpen = false"
      >
        {{ item.label }}
      </RouterLink>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const publicNavItems = [
  { name: 'activities', path: '/activities', label: '課外活動' },
  { name: 'social',     path: '/social',     label: '社會參與' },
  { name: 'literature', path: '/literature', label: '文學天地' },
  { name: 'market',     path: '/market',     label: '市場消息' },
  { name: 'news',       path: '/news',       label: '總經新聞' },
]

const adminNavItems = [
  { name: 'thesis',  path: '/thesis',  label: '論文統整' },
  { name: 'finance', path: '/finance', label: '理財規劃' },
  { name: 'admin',   path: '/admin',   label: '功能管理' },
]

const visibleNavItems = computed(() =>
  auth.isLoggedIn
    ? [...publicNavItems, ...adminNavItems]
    : publicNavItems
)
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background-color: var(--color-primary);
  height: var(--navbar-height);
}

.navbar__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  height: 100%;
  padding: 0 var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar__brand {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.navbar__logo {
  width: 36px;
  height: 36px;
  background-color: var(--color-white);
  border-radius: 50%;
  border: 2px solid var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-ink-1);
  flex-shrink: 0;
}

.navbar__title {
  font-family: var(--font-cjk);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-white);
}

.navbar__nav {
  display: flex;
  align-items: center;
  gap: var(--space-5);
}

.navbar__link {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-white);
  transition: opacity 0.2s;
}

.navbar__link:hover,
.navbar__link--active {
  opacity: 0.7;
}

.navbar__hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  padding: var(--space-2);
}

.navbar__hamburger span {
  display: block;
  width: 22px;
  height: 2px;
  background-color: var(--color-white);
  transition: all 0.3s;
}

.navbar__mobile {
  background-color: var(--color-primary);
  padding: var(--space-4) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.navbar__mobile-link {
  font-family: var(--font-cjk);
  font-size: 15px;
  color: var(--color-white);
}

@media (max-width: 767px) {
  .navbar__nav { display: none; }
  .navbar__hamburger { display: flex; }
  .navbar { height: auto; min-height: var(--navbar-height); }
}
</style>
