<template>
  <div class="swarm-page">
    <DemoModeBanner />
    <div v-if="run.mode === 'demo'" class="curated-banner"><strong>Live persona simulation</strong><span>Nine distinct agents are reacting to the selected concept in real time.</span></div>
    <div class="swarm-layout">
      <div class="arena-card">
        <div class="arena-heading">
          <div><span>{{ topic?.category || 'OASIS simulation' }}</span><h2>{{ topic?.name || 'Live agent swarm' }}</h2><p>{{ topic?.question }}</p></div>
          <div class="heading-actions">
            <button v-if="run.mode === 'demo' && run.isRunning" @click="finishNow">Finish now</button>
            <button v-if="run.mode === 'demo' && !run.isRunning" @click="restart">Restart</button>
            <div class="live-state"><i :class="{ stopped: !run.isRunning }"></i>{{ run.isRunning ? 'LIVE' : 'COMPLETE' }}</div>
          </div>
        </div>
        <div class="arena">
          <div class="mesh"></div>
          <button v-for="agent in visibleAgents" :key="agent.id" class="agent-node" :class="{ thinking: latestAgent === agent.id, selected: selectedAgent === agent.id }" :style="nodeStyle(agent)" @click="selectedAgent = selectedAgent === agent.id ? '' : agent.id">
            <span class="agent-orbit" :style="{ borderColor: agent.color }"></span><span class="agent-core" :style="{ background: agent.color, boxShadow: `0 0 22px ${agent.color}` }"></span><b>{{ initials(agent.name) }}</b>
            <small>{{ agent.name }}</small>
          </button>
          <div v-if="activeThought" class="thought-popover" :style="popoverStyle">
            <span :style="{ color: activeAgent?.color }">{{ activeAgent?.name }} - {{ activeAgent?.segment }}</span>
            <p>"{{ activeThought.action_args.content }}"</p>
          </div>
        </div>
        <div class="progress-row"><div class="progress"><span :style="{ width: `${run.progress}%` }"></span></div><small>Round {{ run.currentRound }} / {{ run.totalRounds }} - {{ run.progress }}%</small></div>
      </div>

      <aside class="feed-panel">
        <div class="feed-title"><span>Agent thoughts</span><b>{{ run.actions.length }}</b></div>
        <div class="feed-list" ref="feedEl">
          <button v-for="action in [...run.actions].reverse()" :key="`${action.agent_id}-${action.timestamp}`" class="feed-item" @click="selectedAgent = action.agent_id">
            <i :style="{ background: agentFor(action.agent_id)?.color || '#7882A0' }"></i>
            <span><strong>{{ action.agent_name }}</strong><small>{{ action.segment }} - Round {{ action.round_num }}</small><p>{{ action.action_args.content }}</p></span>
          </button>
          <div v-if="!run.actions.length" class="waiting"><div class="spinner"></div><strong>Agents are entering the environment</strong><span>First thoughts will appear shortly.</span></div>
        </div>
        <router-link v-if="!run.isRunning" to="/results" class="results-link">Explore results -></router-link>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, reactive, ref } from 'vue'
import DemoModeBanner from '@/components/ui/DemoModeBanner.vue'
import run, { appendDemoThought, completeDemoTopic, launchDemoTopic, refreshRun } from '@/composables/useRun'
import { getDemoTopic } from '@/data/demoTopics'

const selectedAgent = ref('')
const latestAgent = ref('')
const feedEl = ref(null)
const offsets = reactive({})
let thoughtTimer
let movementTimer
let liveTimer

const topic = computed(() => run.mode === 'demo' ? getDemoTopic(run.topicId) : null)
const fallbackAgents = computed(() => run.agentStats.map((agent,index) => ({ id: agent.agent_id, name: agent.agent_name || `Agent ${index + 1}`, segment: agent.segment || 'Persona', color: ['#4B5FA8','#3B7355','#8E6B4E'][index % 3], x: 15 + (index % 3) * 34, y: 22 + Math.floor(index / 3) * 27 })))
const visibleAgents = computed(() => {
  if (!topic.value) return fallbackAgents.value
  const agentIds = run.configuration?.agentIds
  return agentIds?.length ? topic.value.agents.filter(agent => agentIds.includes(agent.id)) : topic.value.agents
})
const activeThought = computed(() => [...run.actions].reverse().find(action => action.agent_id === (selectedAgent.value || latestAgent.value)))
const activeAgent = computed(() => agentFor(selectedAgent.value || latestAgent.value))
const popoverStyle = computed(() => ({ left: `${Math.min(72, Math.max(8, (activeAgent.value?.x || 50) - 8))}%`, top: `${Math.min(68, (activeAgent.value?.y || 50) + 10)}%` }))

function agentFor(id) { return visibleAgents.value.find(agent => agent.id === id) }
function initials(name) { return name.split(' ').map(part => part[0]).join('').slice(0,2) }
function nodeStyle(agent) { const offset = offsets[agent.id] || { x:0,y:0 }; return { left:`${agent.x}%`,top:`${agent.y}%`,transform:`translate(calc(-50% + ${offset.x}px), calc(-50% + ${offset.y}px))` } }
function moveAgents() { visibleAgents.value.forEach(agent => { offsets[agent.id] = { x: Math.round((Math.random() - .5) * 24), y: Math.round((Math.random() - .5) * 18) } }) }
function scheduleThought() {
  if (!topic.value || !run.isRunning) return
  const index = run.actions.length
  const allowedAgentIds = run.configuration?.agentIds
  const thoughtSequence = topic.value.thoughts.map((thought, originalIndex) => ({ thought, originalIndex })).filter(item => !allowedAgentIds?.length || allowedAgentIds.includes(item.thought[0]))
  if (index >= thoughtSequence.length) { completeDemoTopic(topic.value); return }
  thoughtTimer = setTimeout(async () => {
    latestAgent.value = thoughtSequence[index].thought[0]
    appendDemoThought(topic.value, thoughtSequence[index].originalIndex)
    await nextTick(); if (feedEl.value) feedEl.value.scrollTop = 0
    scheduleThought()
  }, index === 0 ? 900 : 1200)
}
function finishNow() {
  if (!topic.value) return
  clearTimeout(thoughtTimer)
  const allowedAgentIds = run.configuration?.agentIds
  const thoughtSequence = topic.value.thoughts.map((thought, originalIndex) => ({ thought, originalIndex })).filter(item => !allowedAgentIds?.length || allowedAgentIds.includes(item.thought[0]))
  for (let index = run.actions.length; index < thoughtSequence.length; index += 1) appendDemoThought(topic.value, thoughtSequence[index].originalIndex)
  latestAgent.value = thoughtSequence.at(-1).thought[0]
  completeDemoTopic(topic.value)
}
function restart() {
  if (!topic.value) return
  clearTimeout(thoughtTimer)
  const topicId = topic.value.id
  const configuration = run.configuration || {}
  launchDemoTopic(topicId, configuration)
  scheduleThought()
}
async function pollLive() { try { await refreshRun() } catch {} if (run.isRunning && run.mode === 'live') liveTimer = setTimeout(pollLive, 1500) }
onMounted(() => {
  if (!run.simulationId && !run.topicId) launchDemoTopic('orbit-note')
  moveAgents(); movementTimer = setInterval(moveAgents, 900)
  if (run.mode === 'demo') scheduleThought(); else pollLive()
})
onUnmounted(() => { clearTimeout(thoughtTimer);clearTimeout(liveTimer);clearInterval(movementTimer) })
</script>

<style scoped>
.swarm-page { display:flex;flex-direction:column;gap:12px;height:100%; }.curated-banner { padding:9px 13px;border-radius:9px;background:#edf6ff;border:1px solid #b8d7f0;color:#315e7b;font-size:12px;display:flex;gap:10px; }.swarm-layout { display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:14px;flex:1;min-height:0; }.arena-card,.feed-panel { background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden; }.arena-card { display:flex;flex-direction:column; }.arena-heading { display:flex;justify-content:space-between;padding:18px 20px; }.arena-heading span { color:var(--accent);text-transform:uppercase;font-size:10px;font-weight:800;letter-spacing:.1em; }.arena-heading h2 { font-size:22px;margin:2px 0; }.arena-heading p { color:var(--text-3);font-size:12px; }.live-state { font-size:10px;font-weight:800;letter-spacing:.1em;display:flex;align-items:center;gap:7px; }.live-state i { width:8px;height:8px;border-radius:50%;background:#e14f4f;box-shadow:0 0 0 5px rgba(225,79,79,.13);animation:pulse 1.2s infinite; }.live-state i.stopped { background:#3B7355;animation:none;box-shadow:none; }
.heading-actions { display:flex;align-items:center;gap:12px; }.heading-actions>button { border:1px solid var(--border);border-radius:7px;padding:6px 10px;color:var(--accent);font-size:11px;font-weight:700; }.heading-actions>button:hover { background:var(--accent-light); }
.arena { position:relative;flex:1;min-height:430px;background:radial-gradient(circle at 50% 45%,#27304b,#111522 72%);overflow:hidden; }.mesh { position:absolute;inset:0;opacity:.16;background-image:linear-gradient(rgba(255,255,255,.15) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.15) 1px,transparent 1px);background-size:34px 34px; }.agent-node { position:absolute;width:74px;height:74px;transition:transform .9s ease;z-index:2;color:white; }.agent-core { position:absolute;left:27px;top:19px;width:20px;height:20px;border-radius:50%; }.agent-orbit { position:absolute;left:19px;top:11px;width:36px;height:36px;border:1px solid;border-radius:50%;opacity:.55; }.agent-node b { position:absolute;left:25px;top:22px;font-size:8px;color:white; }.agent-node small { position:absolute;top:51px;left:50%;transform:translateX(-50%);width:110px;font-size:9px;color:#cbd2e6;white-space:nowrap; }.agent-node.thinking .agent-orbit { animation:orbitPulse .8s infinite alternate; }.agent-node.selected .agent-orbit { border-width:3px;opacity:1; }.thought-popover { position:absolute;width:260px;padding:12px 14px;background:rgba(255,255,255,.96);border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.25);z-index:5;pointer-events:none; }.thought-popover span { font-size:10px;font-weight:800;text-transform:uppercase; }.thought-popover p { font-size:12px;line-height:1.45;margin-top:4px;color:var(--ink); }
.progress-row { padding:12px 18px;display:flex;align-items:center;gap:12px; }.progress { height:6px;background:var(--border);border-radius:8px;flex:1;overflow:hidden; }.progress span { display:block;height:100%;background:var(--accent);transition:width .5s; }.progress-row small { color:var(--text-3); }.feed-panel { display:flex;flex-direction:column; }.feed-title { display:flex;justify-content:space-between;padding:14px;border-bottom:1px solid var(--border);font-weight:700; }.feed-title b { color:var(--accent); }.feed-list { flex:1;overflow:auto;padding:0 12px; }.feed-item { width:100%;display:grid;grid-template-columns:8px 1fr;gap:9px;text-align:left;padding:11px 2px;border-bottom:1px solid var(--border); }.feed-item i { width:7px;height:7px;border-radius:50%;margin-top:5px; }.feed-item span { display:flex;flex-direction:column; }.feed-item small { font-size:9px;color:var(--text-3);text-transform:uppercase; }.feed-item p { font-size:11px;line-height:1.45;color:var(--text-2);margin-top:4px; }.waiting { height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--text-3);gap:5px; }.spinner { width:24px;height:24px;border:2px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin 1s linear infinite;margin-bottom:8px; }.results-link { margin:10px;padding:10px;text-align:center;border-radius:8px;background:var(--accent);color:#fff;font-weight:700;font-size:12px; }
@keyframes pulse { 50% { opacity:.45; } } @keyframes orbitPulse { to { transform:scale(1.35);opacity:.2; } } @keyframes spin { to { transform:rotate(360deg); } }
</style>
