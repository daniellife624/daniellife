<template>
  <div class="home">
    <HeroCard />
    <InternSection />
    <ProjectSection />
    <CertSection />
    <AcademicSection />
    <FuturePlanSection />
  </div>
</template>

<script setup lang="ts">
import HeroCard from '@/components/homepage/HeroCard.vue'
import InternSection from '@/components/homepage/InternSection.vue'
import ProjectSection from '@/components/homepage/ProjectSection.vue'
import CertSection from '@/components/homepage/CertSection.vue'
import AcademicSection from '@/components/homepage/AcademicSection.vue'
import FuturePlanSection from '@/components/homepage/FuturePlanSection.vue'
</script>
