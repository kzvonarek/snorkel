<template>
  <div class="report-page">
    <DemoModeBanner />
    <div class="report-toolbar">
      <div><h2>{{ topic?.name || 'PMF simulation' }} report</h2><p>{{ run.mode === 'demo' ? 'Meeting-ready report based on the completed persona simulation.' : 'Generated from observed simulation activity and agent interviews.' }}</p></div>
      <div class="toolbar-actions">
        <BaseButton v-if="!report" variant="primary" pill :disabled="generating" @click="generate">{{ generating ? 'Generating...' : 'Generate report' }}</BaseButton>
        <a v-if="report && run.mode === 'live'" :href="downloadUrl"><BaseButton variant="secondary" pill>Download Markdown</BaseButton></a>
        <a v-if="report && run.mode === 'demo'" :href="topic.pdfUrl" download><BaseButton variant="primary" pill>Download PDF</BaseButton></a>
        <BaseButton v-if="report && run.mode === 'fixture'" variant="secondary" pill @click="downloadFixture">Download Markdown</BaseButton>
      </div>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
    <div class="report-layout">
      <div class="document">
        <div v-if="generating" class="empty-state"><strong>Report agent is working</strong><span>This can take several minutes for a live run.</span></div>
        <iframe v-else-if="report && topic" class="pdf-preview" :src="`${topic.pdfUrl}#view=FitH&toolbar=0&navpanes=0`" :title="`${topic.name} PMF report preview`"></iframe>
        <pre v-else-if="report" class="markdown">{{ report.markdown_content || 'The report completed without Markdown content.' }}</pre>
        <div v-else class="empty-state"><strong>No report yet</strong><span>Generate a report from the active simulation.</span></div>
      </div>
      <div class="chat-panel">
        <div class="chat-heading">Ask the report</div>
        <div class="messages">
          <div v-for="(message,index) in messages" :key="index" class="message" :class="message.role"><strong>{{ message.role === 'user' ? 'You' : 'Snorkel' }}</strong><span>{{ message.content }}</span></div>
          <div v-if="asking" class="message assistant"><strong>Snorkel</strong><span>Thinking...</span></div>
        </div>
        <form class="chat-form" @submit.prevent="ask">
          <input v-model="question" :disabled="!report || asking" placeholder="Ask about evidence, objections, or segments" />
          <button :disabled="!report || asking">Send</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import DemoModeBanner from '@/components/ui/DemoModeBanner.vue'
import run, { askReport, buildReport } from '@/composables/useRun'
import { reportDownloadUrl } from '@/api/report'
import { getDemoTopic } from '@/data/demoTopics'

const report = computed(() => run.report)
const topic = computed(() => run.mode === 'demo' ? getDemoTopic(run.topicId) : null)
const generating = ref(false)
const asking = ref(false)
const error = ref('')
const question = ref('')
const messages = ref([])
const downloadUrl = computed(() => reportDownloadUrl(run.reportId))

async function generate() {
  generating.value = true; error.value = ''
  try { await buildReport() } catch (err) { error.value = err.message }
  finally { generating.value = false }
}
async function ask() {
  const text = question.value.trim(); if (!text) return
  messages.value.push({ role: 'user', content: text }); question.value = ''; asking.value = true
  try {
    const history = messages.value.slice(0,-1).map(item => ({ role: item.role, content: item.content }))
    const [result] = await Promise.all([
      askReport(text, history),
      new Promise(resolve => setTimeout(resolve, 2200)),
    ])
    messages.value.push({ role: 'assistant', content: result.response || result.message || 'No response returned.' })
  } catch (err) { messages.value.push({ role: 'assistant', content: `Unable to answer: ${err.message}` }) }
  finally { asking.value = false }
}
function downloadFixture() {
  const blob = new Blob([report.value.markdown_content], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob); const link = document.createElement('a')
  link.href = url; link.download = 'snorkel-demo-report.md'; link.click(); URL.revokeObjectURL(url)
}
</script>

<style scoped>
.report-page { display:flex;flex-direction:column;gap:14px;height:100%; }.report-toolbar { display:flex;justify-content:space-between;align-items:center; }.report-toolbar p { color:var(--text-3);font-size:12px;margin-top:3px; }.toolbar-actions { display:flex;gap:8px; }.report-layout { display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px;min-height:0;flex:1; }.document,.chat-panel { background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-card);overflow:hidden; }.document { min-height:680px;background:#353a46; }.pdf-preview { display:block;width:100%;height:100%;min-height:680px;border:0;background:white; }.markdown { font-family:inherit;white-space:pre-wrap;line-height:1.7;font-size:13px;padding:32px;background:white;height:100%;overflow:auto; }.empty-state { height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:var(--text-3);background:white; }.empty-state strong { color:var(--ink); }.chat-panel { display:flex;flex-direction:column; }.chat-heading { padding:13px;border-bottom:1px solid var(--border);font-weight:700; }.messages { flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:10px; }.message { display:flex;flex-direction:column;gap:3px;padding:9px;border-radius:8px;background:var(--bg);font-size:12px; }.message.user { background:var(--accent-light); }.chat-form { display:flex;gap:6px;padding:10px;border-top:1px solid var(--border); }.chat-form input { min-width:0;flex:1;padding:9px;border:1px solid var(--border);border-radius:7px; }.chat-form button { padding:0 12px;background:var(--accent);color:white;border-radius:7px; }.error { padding:10px;border:1px solid #c44a4a;color:#8e2828;border-radius:8px;background:#fff0f0; }
</style>
