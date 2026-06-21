<template>
  <div class="personas">
    <div v-if="topic" class="study-banner"><span :style="{ background: topic.color }"></span><div><strong>{{ topic.name }}</strong><small>Personas derived for this study</small></div></div>
    <div v-if="!personas.length" class="empty-state"><strong>No personas added yet</strong><span>Add customer segments or connect data sources to build this study.</span><BaseButton variant="secondary">Add persona</BaseButton></div>
    <div
      v-for="p in personas"
      :key="p.id"
      class="persona-row"
      :class="{ expanded: p.expanded }"
    >
      <div class="persona-header" @click="p.expanded = !p.expanded">
        <div class="persona-swatch" :style="{ background: p.color }"></div>
        <div class="persona-main">
          <div class="persona-name">{{ p.name }}</div>
          <div class="persona-traits">
            <span v-for="t in p.traits" :key="t" class="trait-chip">{{ t }}</span>
          </div>
        </div>
        <div class="persona-meta">
          <span class="persona-size">{{ p.size }}</span>
          <StatusBadge :label="p.confidence" :variant="p.confidence" />
        </div>
        <div class="expand-icon">{{ p.expanded ? '▲' : '▼' }}</div>
      </div>

      <div v-if="p.expanded" class="persona-detail">
        <div class="detail-sources">
          <div class="detail-heading">Aggregated from</div>
          <div v-for="s in p.sources" :key="s.label" class="source-row">
            <span class="source-label">{{ s.label }}</span>
            <ProgressBar :value="s.pct" style="flex:1" />
            <span class="source-pct">{{ s.pct }}%</span>
          </div>
        </div>

        <div class="detail-quote">
          <div class="detail-heading">Representative signal</div>
          <blockquote>{{ p.quote }}</blockquote>
        </div>

        <div class="detail-actions">
          <BaseButton variant="ghost">Split</BaseButton>
          <BaseButton variant="ghost">Merge</BaseButton>
          <BaseButton variant="secondary">Edit persona</BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import run from '@/composables/useRun'
import { getDemoTopic } from '@/data/demoTopics'
import { getStudyInputs } from '@/data/studyInputs'

const topic = run.topicId ? getDemoTopic(run.topicId) : null
const personas = reactive(JSON.parse(JSON.stringify(topic ? getStudyInputs(topic.id).personas : [])))
</script>

<style scoped>
.personas { display: flex; flex-direction: column; gap: 10px; }
.study-banner { display:flex;align-items:center;gap:10px;padding:11px 14px;background:var(--surface);border:1px solid var(--border);border-radius:10px;margin-bottom:4px; }.study-banner>span { width:10px;height:32px;border-radius:5px; }.study-banner div { display:flex;flex-direction:column; }.study-banner small { color:var(--text-3); }.empty-state { padding:48px;border:1px dashed var(--border-2);border-radius:12px;display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--text-3); }.empty-state strong { color:var(--ink); }

.persona-row {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  overflow: hidden;
  transition: box-shadow 0.15s;
}
.persona-row.expanded { box-shadow: var(--shadow-md); }

.persona-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 18px;
  cursor: pointer;
  user-select: none;
}
.persona-header:hover { background: var(--bg); }

.persona-swatch { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.persona-main   { flex: 1; }
.persona-name   { font-size: 14px; font-weight: 700; color: var(--ink); margin-bottom: 4px; }

.persona-traits { display: flex; gap: 6px; flex-wrap: wrap; }

.trait-chip {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-pill);
  background: var(--bg);
  color: var(--text-2);
  border: 1px solid var(--border);
}

.persona-meta  { display: flex; align-items: center; gap: 10px; }
.persona-size  { font-size: 12px; color: var(--text-3); }
.expand-icon   { font-size: 10px; color: var(--text-3); width: 16px; text-align: center; }

.persona-detail {
  border-top: 1px solid var(--border);
  padding: 18px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.detail-heading {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-3);
  margin-bottom: 10px;
}

.source-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.source-label { font-size: 12px; color: var(--text-2); width: 130px; flex-shrink: 0; }
.source-pct   { font-size: 12px; font-weight: 600; color: var(--text-2); width: 32px; text-align: right; }

blockquote {
  font-size: 13px;
  color: var(--text-2);
  line-height: 1.6;
  border-left: 3px solid var(--accent);
  padding-left: 12px;
  font-style: italic;
}

.detail-actions {
  grid-column: span 2;
  display: flex;
  gap: 8px;
}
</style>
