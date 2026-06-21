<template>
  <div class="results">
    <div class="stats-row">
      <StatCard label="PMF Score" :value="stats.pmfScore" sub="out of 100" dark />
      <StatCard label="Would Recommend" :value="stats.recommendPct + '%'" sub="Net promoter signal" />
      <StatCard label="Top Objections" :value="stats.objectionCount" sub="across all segments" />
      <StatCard label="Adoption Rate" :value="stats.adoptionRate + '%'" sub="conversion from trial" />
    </div>

    <BaseCard>
      <div class="card-heading">Sentiment by segment</div>
      <BarChartCss :rows="sentimentBySegment" />
    </BaseCard>

    <BaseCard>
      <div class="card-heading">Adoption by segment × tier</div>
      <Heatmap :cols="adoptionHeatmap.cols" :rows="adoptionHeatmap.rows" />
    </BaseCard>

    <BaseCard>
      <div class="card-heading">Ranked objections</div>
      <div class="objections-list">
        <div v-for="obj in topObjections" :key="obj.rank" class="objection-row">
          <div class="obj-rank">#{{ obj.rank }}</div>
          <div class="obj-text">{{ obj.text }}</div>
          <div class="obj-meta">
            <span class="obj-freq">{{ obj.frequency }}x</span>
            <StatusBadge :label="obj.severity" :variant="severityVariant(obj.severity)" />
          </div>
        </div>
      </div>
    </BaseCard>

    <BaseCard>
      <div class="card-heading">vs. Competitors (overall PMF score)</div>
      <BarChartCss :rows="vsCompetitor" />
    </BaseCard>

    <div class="results-cta">
      <router-link to="/report">
        <BaseButton variant="primary" pill>Build report →</BaseButton>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import StatCard from '@/components/ui/StatCard.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BarChartCss from '@/components/ui/BarChartCss.vue'
import Heatmap from '@/components/ui/Heatmap.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { stats, sentimentBySegment, adoptionHeatmap, topObjections, vsCompetitor } from '@/data/results.js'

function severityVariant(s) {
  if (s === 'high') return 'low'
  if (s === 'med')  return 'med'
  return 'high'
}
</script>

<style scoped>
.results { display: flex; flex-direction: column; gap: 20px; }

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.card-heading {
  font-size: 13px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 16px;
}

.objections-list { display: flex; flex-direction: column; }

.objection-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 11px 0;
  border-bottom: 1px solid var(--border);
}
.objection-row:last-child { border-bottom: none; }

.obj-rank  { font-size: 12px; font-weight: 700; color: var(--text-3); width: 24px; flex-shrink: 0; }
.obj-text  { flex: 1; font-size: 13px; color: var(--ink); }
.obj-meta  { display: flex; align-items: center; gap: 8px; }
.obj-freq  { font-size: 12px; font-weight: 600; color: var(--text-3); }

.results-cta { display: flex; justify-content: flex-end; }
</style>
