<template>
  <footer class="footer">
    <p>© 2026 daniellife｜Designed & Developed by 周彥廷<span class="footer__en"> / Yen-Ting Chou</span></p>
  </footer>
</template>

<script setup lang="ts">
</script>

<style scoped>
.footer {
  background-color: var(--color-ink-1);
  color: var(--color-ink-3);
  text-align: center;
  padding: 8px var(--space-6);
  font-size: 12px;
  font-family: var(--font-body);
}

@media (max-width: 767px) {
  .footer__en { display: none; }
}
</style>
