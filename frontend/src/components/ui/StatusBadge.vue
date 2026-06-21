<template>
  <span class="badge" :class="`badge--${variant}`">{{ label }}</span>
</template>

<script setup>
defineProps({
  label:   { type: String, required: true },
  variant: { type: String, default: 'neutral' },
  // confidence: high | med | low
  // status: ready | running | draft
})
</script>

<style scoped>
.badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: var(--radius-pill);
  letter-spacing: 0.03em;
  text-transform: capitalize;
}

.badge--high,
.badge--ready   { background: var(--success-bg); color: var(--success-fg); }
.badge--med,
.badge--running { background: var(--warn-bg);    color: var(--warn-fg); }
.badge--low,
.badge--draft   { background: var(--neg-bg);     color: var(--neg-fg); }
.badge--neutral { background: var(--bg);          color: var(--text-2); border: 1px solid var(--border); }
</style>
