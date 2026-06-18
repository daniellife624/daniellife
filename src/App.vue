<template>
  <AppNavbar />
  <main>
    <RouterView />
  </main>
  <AppFooter />
</template>

<script setup lang="ts">
import AppNavbar from '@/components/common/AppNavbar.vue'
import AppFooter from '@/components/common/AppFooter.vue'
</script>

<style scoped>
main {
  min-height: calc(100vh - var(--navbar-height));
  padding-top: var(--navbar-height);
}
</style>