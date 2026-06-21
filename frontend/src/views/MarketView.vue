<template>
  <div class="market">
    <div v-if="topic" class="study-banner"><span :style="{ background: topic.color }"></span><div><strong>{{ topic.name }}</strong><small>Competitive and environmental context</small></div></div>
    <DropZone
      label="Drop competitive intelligence files here"
      sub="PDF, DOCX, PNG — market reports, analyst decks, competitor reviews"
      @files="addFiles"
    />

    <div v-if="envs.length" class="env-section">
      <div class="env-heading">Environment cards</div>
      <div class="env-grid">
        <div
          v-for="env in envs"
          :key="env.id"
          class="env-card"
          draggable="true"
        >
          <div class="env-type-badge">{{ env.type }}</div>
          <div class="env-name">{{ env.name }}</div>
          <div class="env-notes">{{ env.notes }}</div>
          <div class="env-tags">
            <span v-for="t in env.tags" :key="t" class="env-tag">{{ t }}</span>
          </div>
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
const envs = reactive([...(topic ? getStudyInputs(topic.id).market : [])])

function addFiles(files) {
  files.forEach(f => {
    envs.push({
      id: 'uploaded-' + Date.now(),
      name: f.name,
      type: 'Uploaded',
      notes: 'Manually uploaded — will be parsed by agents.',
      tags: ['User uploaded'],
    })
  })
}
</script>

<style scoped>
.market { display: flex; flex-direction: column; gap: 28px; }
.study-banner { display:flex;align-items:center;gap:10px;padding:11px 14px;background:var(--surface);border:1px solid var(--border);border-radius:10px; }.study-banner>span { width:10px;height:32px;border-radius:5px; }.study-banner div { display:flex;flex-direction:column; }.study-banner small { color:var(--text-3); }

.env-heading { font-size: 13px; font-weight: 700; color: var(--ink); margin-bottom: 12px; }

.env-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.env-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px;
  cursor: grab;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: box-shadow 0.15s;
}
.env-card:hover { box-shadow: var(--shadow-md); }

.env-type-badge {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent);
}
.env-name  { font-size: 13.5px; font-weight: 700; color: var(--ink); }
.env-notes { font-size: 12px; color: var(--text-2); line-height: 1.45; }

.env-tags  { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.env-tag {
  font-size: 10px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: var(--radius-pill);
  background: var(--bg);
  color: var(--text-3);
  border: 1px solid var(--border);
}
</style>
