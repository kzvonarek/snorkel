<template>
  <div v-if="run.mode === 'fixture'" class="demo-banner">
    <strong>Demo data</strong>
    <span>{{ run.fixtureReason }} Results below are deterministic fixtures, not a live OASIS run.</span>
  </div>
</template>

<script setup>
import run from '@/composables/useRun'
</script>

<style scoped>
.demo-banner { display: flex; gap: 10px; align-items: center; padding: 10px 14px; border: 1px solid #d5a43b; border-radius: 9px; background: #fff7df; color: #6f4d00; font-size: 12px; }
.demo-banner strong { text-transform: uppercase; letter-spacing: .06em; white-space: nowrap; }
</style>
