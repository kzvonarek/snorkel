<template>
  <div class="bar-chart">
    <div v-for="row in rows" :key="row.label" class="bar-row">
      <div class="bar-label">{{ row.label }}</div>
      <div class="bar-track">
        <div
          class="bar-fill"
          :style="{ width: row.pct + '%', background: color(row.sentiment) }"
        ></div>
      </div>
      <div class="bar-value">{{ row.pct }}%</div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  rows: {
    type: Array,
    default: () => [],
    // [{ label, pct, sentiment: 'pos'|'neu'|'neg' }]
  },
})

function color(sentiment) {
  if (sentiment === 'pos') return 'var(--success-fg)'
  if (sentiment === 'neg') return 'var(--neg-fg)'
  return 'var(--warn-fg)'
}
</script>

<style scoped>
.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.bar-row {
  display: grid;
  grid-template-columns: 130px 1fr 40px;
  align-items: center;
  gap: 10px;
}

.bar-label {
  font-size: 12.5px;
  color: var(--text-2);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bar-track {
  height: 8px;
  border-radius: 4px;
  background: var(--border);
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.bar-value {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-2);
  text-align: right;
}
</style>
