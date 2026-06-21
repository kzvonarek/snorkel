<template>
  <div class="sandbox">
    <!-- Tray -->
    <div class="tray">
      <div class="tray-heading">Segments</div>
      <div v-for="p in personas" :key="p.id" class="tray-item" draggable="true" @dragstart="onDragStart($event, p, 'segment')">
        <div class="tray-dot" :style="{ background: p.color }"></div>
        {{ p.name }}
      </div>

      <div class="tray-heading">Environments</div>
      <div v-for="e in environments" :key="e.id" class="tray-item" draggable="true" @dragstart="onDragStart($event, e, 'environment')">
        ◈ {{ e.name }}
      </div>

      <div class="tray-heading">Product assets</div>
      <div v-for="a in products" :key="a.id" class="tray-item" draggable="true" @dragstart="onDragStart($event, a, 'product')">
        ⬕ {{ a.name }}
      </div>
    </div>

    <!-- Canvas -->
    <div class="canvas" @dragover.prevent @drop.prevent="onDrop">
      <div
        v-for="node in canvasNodes"
        :key="node.id"
        class="canvas-node"
        :style="{ left: node.x + 'px', top: node.y + 'px' }"
      >
        <div class="node-type">{{ node.type }}</div>
        <div class="node-name">{{ node.name }}</div>
      </div>
      <div v-if="!canvasNodes.length" class="canvas-empty">
        Drag segments, environments &amp; product assets here
      </div>
    </div>

    <!-- Run settings -->
    <div class="run-settings">
      <div class="settings-heading">Run settings</div>
      <Slider v-model="rounds" label="Simulation rounds" :min="1" :max="10" />
      <Slider v-model="agentsPerSegment" label="Agents / segment" :min="1" :max="20" />

      <div class="mode-row">
        <span class="settings-label">Mode</span>
        <div class="mode-toggle">
          <button :class="{ active: mode === 'social' }"    @click="mode = 'social'">Social</button>
          <button :class="{ active: mode === 'interview' }" @click="mode = 'interview'">Interview</button>
        </div>
      </div>

      <div class="cost-estimate">
        <div class="cost-label">Est. cost</div>
        <div class="cost-value">${{ costEstimate.toFixed(2) }}</div>
      </div>

      <div v-if="runError" class="run-error">{{ runError }}</div>
      <BaseButton variant="primary" pill style="width:100%;justify-content:center;" :disabled="launching" @click="runSim">
        Run simulation →
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import Slider from '@/components/ui/Slider.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import run, { launchRun } from '@/composables/useRun.js'
import { getStudyInputs } from '@/data/studyInputs'

const router = useRouter()
const inputs = getStudyInputs(run.topicId)
const personas = inputs.personas
const environments = inputs.market
const products = inputs.products
const canvasNodes = reactive([])
const rounds = ref(5)
const agentsPerSegment = ref(5)
const mode = ref('social')
const launching = ref(false)
const runError = ref('')

const costEstimate = computed(() => rounds.value * agentsPerSegment.value * personas.length * 0.004)

let dragItem = null

function onDragStart(e, item, type) {
  dragItem = { ...item, type }
}

function onDrop(e) {
  if (!dragItem) return
  const rect = e.currentTarget.getBoundingClientRect()
  canvasNodes.push({
    id: dragItem.id + '-' + Date.now(),
    sourceId: dragItem.id,
    name: dragItem.name,
    type: dragItem.type,
    x: e.clientX - rect.left - 65,
    y: e.clientY - rect.top - 20,
  })
  dragItem = null
}

async function runSim() {
  const selectedPersonas = canvasNodes.filter(node => node.type === 'segment').map(node => personas.find(item => item.id === node.sourceId)).filter(Boolean)
  const selectedProducts = canvasNodes.filter(node => node.type === 'product').map(node => products.find(item => item.id === node.sourceId)).filter(Boolean)
  const selectedEnvironments = canvasNodes.filter(node => node.type === 'environment').map(node => environments.find(item => item.id === node.sourceId)).filter(Boolean)
  if (!selectedPersonas.length || !selectedProducts.length) {
    runError.value = 'Add at least one persona segment and one product asset to the canvas.'
    return
  }
  launching.value = true
  runError.value = ''
  await launchRun({ product: selectedProducts[0], environments: selectedEnvironments, personas: selectedPersonas, rounds: rounds.value, agentsPerSegment: agentsPerSegment.value })
  launching.value = false
  router.push('/swarm')
}
</script>

<style scoped>
.sandbox {
  display: grid;
  grid-template-columns: 190px 1fr 200px;
  gap: 16px;
  height: calc(100vh - var(--topbar-h) - 56px);
}

.tray {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 14px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tray-heading {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-3);
  margin-top: 10px;
  margin-bottom: 4px;
}
.tray-heading:first-child { margin-top: 0; }

.tray-item {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 12.5px;
  color: var(--text-2);
  padding: 6px 8px;
  border-radius: 7px;
  border: 1px solid var(--border);
  cursor: grab;
  background: var(--bg);
  user-select: none;
}
.tray-item:hover { border-color: var(--accent); color: var(--accent); }

.tray-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

.canvas {
  background:
    linear-gradient(0deg, transparent 23px, var(--border) 24px),
    linear-gradient(90deg, transparent 23px, var(--border) 24px);
  background-size: 24px 24px;
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  position: relative;
  overflow: hidden;
}

.canvas-empty {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  color: var(--text-3);
  pointer-events: none;
}

.canvas-node {
  position: absolute;
  width: 130px;
  background: var(--surface);
  border: 1.5px solid var(--border-2);
  border-radius: 8px;
  padding: 8px 10px;
  box-shadow: var(--shadow-card);
  cursor: default;
}
.node-type { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--accent); margin-bottom: 2px; }
.node-name { font-size: 12px; font-weight: 600; color: var(--ink); }

.run-settings {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.settings-heading { font-size: 13px; font-weight: 700; color: var(--ink); }
.settings-label   { font-size: 12.5px; font-weight: 600; color: var(--ink); }

.mode-row { display: flex; flex-direction: column; gap: 8px; }

.mode-toggle {
  display: flex;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
.mode-toggle button {
  flex: 1;
  padding: 6px 4px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-2);
  background: transparent;
  cursor: pointer;
  transition: background 0.12s, color 0.12s;
}
.mode-toggle button.active { background: var(--accent); color: #fff; }

.cost-estimate {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg);
  border-radius: 8px;
  padding: 10px 12px;
}
.cost-label { font-size: 12px; color: var(--text-3); font-weight: 600; }
.cost-value { font-size: 16px; font-weight: 700; color: var(--ink); }
</style>
