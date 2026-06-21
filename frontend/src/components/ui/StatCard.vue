<template>
  <div class="stat-card" :class="{ 'stat-card--dark': dark }">
    <div class="stat-label">{{ label }}</div>
    <div class="stat-value">{{ value }}</div>
    <div v-if="sub" class="stat-sub">{{ sub }}</div>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  sub:   { type: String, default: '' },
  dark:  { type: Boolean, default: false },
})
</script>

<style scoped>
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 20px 22px;
  box-shadow: var(--shadow-card);
}

.stat-card--dark {
  background: var(--ink);
  border-color: transparent;
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-3);
  margin-bottom: 8px;
}

.stat-card--dark .stat-label { color: rgba(255,255,255,0.55); }

.stat-value {
  font-family: 'Newsreader', serif;
  font-size: 38px;
  font-weight: 600;
  color: var(--ink);
  line-height: 1;
}

.stat-card--dark .stat-value { color: #fff; }

.stat-sub {
  font-size: 12px;
  color: var(--text-3);
  margin-top: 6px;
}

.stat-card--dark .stat-sub { color: rgba(255,255,255,0.45); }
</style>
