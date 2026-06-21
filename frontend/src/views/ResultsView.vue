<template>
  <div class="results">
    <DemoModeBanner />
    <div v-if="topic" class="topic-summary" :style="{ borderColor: topic.color }">
      <div><span>{{ topic.category }} - Persona simulation</span><h2>{{ topic.name }}</h2><p>{{ topic.question }}</p></div>
      <div class="fit-score"><strong>{{ topic.metrics.fit }}</strong><small>fit signal</small></div>
    </div>
    <div class="stats-row">
      <StatCard label="Observed thoughts" :value="run.actions.length" sub="recorded in this run" dark />
      <StatCard label="Active personas" :value="run.agentStats.length" sub="individual simulated agents" />
      <StatCard :label="topic ? 'Positive reactions' : 'Posts'" :value="topic ? topic.metrics.positive : postCount" sub="observable signals" />
      <StatCard :label="topic ? 'Pilot intent' : 'Completed rounds'" :value="topic ? `${topic.metrics.pilot}/${topic.agents.length}` : run.currentRound" :sub="topic ? 'personas willing to test' : `of ${run.totalRounds || '-'} configured`" />
    </div>
    <BaseCard>
      <div class="card-heading">Action distribution</div>
      <BarChartCss :rows="actionRows" />
      <div v-if="!actionRows.length" class="empty">No actions have been observed.</div>
    </BaseCard>
    <BaseCard v-if="topic">
      <div class="card-heading">Leading objections</div>
      <div v-for="(objection,index) in topic.objections" :key="objection" class="objection"><b>#{{ index + 1 }}</b><span>{{ objection }}</span></div>
      <div class="recommendation"><strong>Recommended next move</strong><p>{{ topic.recommendation }}</p></div>
    </BaseCard>
    <BaseCard>
      <div class="card-heading">Agent activity</div>
      <div class="activity-table">
        <div v-for="agent in sortedAgents" :key="agent.agent_id" class="activity-row">
          <strong>{{ agent.agent_name || `Agent ${agent.agent_id}` }}</strong>
          <span>{{ agent.total_actions || 0 }} actions</span>
          <code>{{ formatTypes(agent.action_types) }}</code>
        </div>
      </div>
    </BaseCard>
    <BaseCard>
      <div class="card-heading">Observed qualitative signals</div>
      <div v-for="(action,index) in qualitativeActions" :key="index" class="signal"><strong>{{ action.agent_name || `Agent ${action.agent_id}` }}</strong><span>{{ action.action_args?.content || action.action_args?.text }}</span></div>
      <div v-if="!qualitativeActions.length" class="empty">No text reactions were recorded. Generate the report for deeper synthesis.</div>
    </BaseCard>
    <div class="results-cta"><router-link to="/report"><BaseButton variant="primary" pill>Build report -></BaseButton></router-link></div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import StatCard from '@/components/ui/StatCard.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BarChartCss from '@/components/ui/BarChartCss.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import DemoModeBanner from '@/components/ui/DemoModeBanner.vue'
import run, { refreshRun } from '@/composables/useRun'
import { getDemoTopic } from '@/data/demoTopics'

onMounted(() => refreshRun().catch(() => {}))
const topic = computed(() => run.mode === 'demo' ? getDemoTopic(run.topicId) : null)
const postCount = computed(() => run.actions.filter(item => item.action_type === 'CREATE_POST').length)
const sortedAgents = computed(() => [...run.agentStats].sort((a,b) => (b.total_actions || 0) - (a.total_actions || 0)))
const qualitativeActions = computed(() => run.actions.filter(item => item.action_args?.content || item.action_args?.text).slice(-12).reverse())
const actionRows = computed(() => {
  const counts = run.actions.reduce((all,item) => ({ ...all, [item.action_type || 'OTHER']: (all[item.action_type || 'OTHER'] || 0) + 1 }), {})
  const max = Math.max(1, ...Object.values(counts))
  return Object.entries(counts).map(([label,value]) => ({ label: label.replaceAll('_',' '), pct: Math.round(value / max * 100), sentiment: 'pos' }))
})
function formatTypes(types = {}) { return Object.entries(types).map(([name,count]) => `${name.replaceAll('_',' ')}: ${count}`).join(' | ') || 'No action breakdown' }
</script>

<style scoped>
.results { display:flex;flex-direction:column;gap:20px; }.topic-summary { border:1px solid;border-left-width:5px;border-radius:12px;background:var(--surface);padding:18px 20px;display:flex;justify-content:space-between;align-items:center; }.topic-summary span { font-size:10px;color:var(--text-3);text-transform:uppercase;letter-spacing:.1em; }.topic-summary h2 { margin:3px 0; }.topic-summary p { color:var(--text-2); }.fit-score { display:flex;flex-direction:column;align-items:center; }.fit-score strong { font-family:Newsreader,serif;font-size:42px;color:var(--accent);line-height:1; }.fit-score small { color:var(--text-3); }.stats-row { display:grid;grid-template-columns:repeat(4,1fr);gap:16px; }.card-heading { font-size:13px;font-weight:700;margin-bottom:16px; }.activity-row { display:grid;grid-template-columns:1fr 110px 2fr;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);font-size:12px; }.activity-row code { white-space:normal;color:var(--text-2); }.signal { display:grid;grid-template-columns:180px 1fr;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);font-size:12px; }.signal span,.empty { color:var(--text-3); }.objection { display:flex;gap:12px;padding:9px 0;border-bottom:1px solid var(--border); }.objection b { color:var(--accent); }.recommendation { margin-top:16px;padding:14px;background:var(--accent-light);border-radius:9px; }.recommendation p { margin-top:4px;color:var(--text-2); }.results-cta { display:flex;justify-content:flex-end; }
</style>
