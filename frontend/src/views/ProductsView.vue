<template>
  <div class="products">
    <div v-if="topic" class="study-banner"><span :style="{ background: topic.color }"></span><div><strong>{{ topic.name }}</strong><small>Product materials used in this simulation</small></div></div>
    <DropZone
      label="Drop product materials here"
      sub="Specs, pitch decks, Figma exports, prototypes — PDF, DOCX, PNG"
      @files="addAssets"
    />

    <div class="asset-grid">
      <div v-for="a in assets" :key="a.id" class="asset-card">
        <div class="asset-format-badge" :class="`fmt-${a.format.toLowerCase()}`">{{ a.format }}</div>
        <div class="asset-name">{{ a.name }}</div>
        <div class="asset-meta">
          <span class="asset-version">{{ a.version }}</span>
          <span class="asset-dot">·</span>
          <span>{{ a.uploadedAt }}</span>
          <span class="asset-dot">·</span>
          <span>{{ a.size }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import DropZone from '@/components/ui/DropZone.vue'
import run from '@/composables/useRun'
import { getDemoTopic } from '@/data/demoTopics'
import { getStudyInputs } from '@/data/studyInputs'

const topic = run.topicId ? getDemoTopic(run.topicId) : null
const assets = reactive([...(topic ? getStudyInputs(topic.id).products : [])])

function addAssets(files) {
  files.forEach(f => {
    const ext = f.name.split('.').pop().toUpperCase()
    assets.push({
      id: 'up-' + Date.now(),
      name: f.name,
      format: ext,
      version: 'v1.0',
      uploadedAt: 'just now',
      size: (f.size / 1024).toFixed(0) + ' KB',
    })
  })
}
</script>

<style scoped>
.products { display: flex; flex-direction: column; gap: 24px; }
.study-banner { display:flex;align-items:center;gap:10px;padding:11px 14px;background:var(--surface);border:1px solid var(--border);border-radius:10px; }.study-banner>span { width:10px;height:32px;border-radius:5px; }.study-banner div { display:flex;flex-direction:column; }.study-banner small { color:var(--text-3); }

.asset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 12px;
}

.asset-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: box-shadow 0.15s;
}
.asset-card:hover { box-shadow: var(--shadow-md); }

.asset-format-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.05em;
  padding: 2px 7px;
  border-radius: 4px;
  align-self: flex-start;
}
.fmt-pdf  { background: #f2dbd2; color: #ab5238; }
.fmt-docx { background: #dceef7; color: #2d6b91; }
.fmt-png  { background: #def0e7; color: #3b7355; }
.fmt-csv  { background: #f3e7cc; color: #b07f33; }

.asset-name { font-size: 13.5px; font-weight: 700; color: var(--ink); }

.asset-meta {
  font-size: 11px;
  color: var(--text-3);
  display: flex;
  gap: 5px;
  align-items: center;
}
.asset-version { font-weight: 600; color: var(--accent); }
.asset-dot     { opacity: 0.4; }
</style>
