<template>
  <div class="progress-track">
    <div class="progress-fill" :style="{ width: pct + '%', background: color }"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  value: { type: Number, default: 0 },  // 0–100
  max:   { type: Number, default: 100 },
  color: { type: String, default: 'var(--accent)' },
})
const pct = computed(() => Math.min(100, (props.value / props.max) * 100))
</script>

<style scoped>
.progress-track {
  height: 6px;
  border-radius: 3px;
  background: var(--border);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}
</style>
