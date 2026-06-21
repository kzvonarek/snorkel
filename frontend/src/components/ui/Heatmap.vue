<template>
  <div class="heatmap">
    <div class="heatmap-header">
      <div class="heatmap-corner"></div>
      <div v-for="col in cols" :key="col" class="heatmap-col-label">{{ col }}</div>
    </div>
    <div v-for="row in rows" :key="row.label" class="heatmap-row">
      <div class="heatmap-row-label">{{ row.label }}</div>
      <div
        v-for="(cell, ci) in row.cells"
        :key="ci"
        class="heatmap-cell"
        :style="{ background: cellBg(cell), color: cellFg(cell) }"
        :title="`${row.label} × ${cols[ci]}: ${cell}`"
      >{{ cell }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  cols: { type: Array, default: () => [] },
  rows: { type: Array, default: () => [] },
  // rows: [{ label, cells: ['High'|'Med'|'Low'|'—'] }]
})

function cellBg(v) {
  if (v === 'High') return 'var(--success-bg)'
  if (v === 'Med')  return 'var(--warn-bg)'
  if (v === 'Low')  return 'var(--neg-bg)'
  return 'var(--bg)'
}
function cellFg(v) {
  if (v === 'High') return 'var(--success-fg)'
  if (v === 'Med')  return 'var(--warn-fg)'
  if (v === 'Low')  return 'var(--neg-fg)'
  return 'var(--text-3)'
}
</script>

<style scoped>
.heatmap { display: flex; flex-direction: column; gap: 4px; }

.heatmap-header,
.heatmap-row {
  display: grid;
  grid-template-columns: 120px repeat(var(--cols, 4), 1fr);
  gap: 4px;
  align-items: center;
}

.heatmap-corner { }

.heatmap-col-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-3);
  text-align: center;
  padding: 4px 2px;
}

.heatmap-row-label {
  font-size: 12.5px;
  color: var(--text-2);
  padding-right: 8px;
}

.heatmap-cell {
  font-size: 11px;
  font-weight: 600;
  text-align: center;
  padding: 6px 4px;
  border-radius: 6px;
}
</style>
