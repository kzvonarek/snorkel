<template>
  <div class="base-card" :style="accentStyle">
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  accent: { type: String, default: '' },
  padding: { type: String, default: '20px' },
})
const accentStyle = computed(() => ({
  borderLeft: props.accent ? `3px solid ${props.accent}` : undefined,
  padding: props.padding,
}))
</script>

<style scoped>
.base-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}
</style>
