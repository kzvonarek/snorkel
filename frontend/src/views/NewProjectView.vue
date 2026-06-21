<template>
  <div class="new-project">
    <div class="intro">
      <span>Blank study</span>
      <h2>Start with your product idea</h2>
      <p>Add only what you know today. Customer data, personas, market context, and product material can be added in the next steps.</p>
    </div>

    <form class="builder" @submit.prevent="continueSetup">
      <label>
        <span>Project name</span>
        <input v-model="draft.name" required placeholder="e.g. Mobile onboarding redesign" />
      </label>
      <label>
        <span>Product or concept</span>
        <textarea v-model="draft.concept" required rows="4" placeholder="What are you considering building or changing?"></textarea>
      </label>
      <div class="two-col">
        <label>
          <span>Target audience</span>
          <input v-model="draft.audience" placeholder="Who should react to this concept?" />
        </label>
        <label>
          <span>Primary research question</span>
          <input v-model="draft.question" placeholder="What decision should this simulation inform?" />
        </label>
      </div>
      <label>
        <span>Starting context</span>
        <textarea v-model="draft.context" rows="5" placeholder="Paste customer evidence, constraints, market notes, or links. This can be left blank."></textarea>
      </label>

      <div class="next-steps">
        <strong>Next, build the study</strong>
        <div><span>1</span>Connect customer signals</div>
        <div><span>2</span>Review or add personas</div>
        <div><span>3</span>Add market and product material</div>
        <div><span>4</span>Configure and run the simulation</div>
      </div>

      <div class="actions">
        <router-link to="/projects">Cancel</router-link>
        <BaseButton type="submit" variant="primary" pill>Save and add data -></BaseButton>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/ui/BaseButton.vue'
import { resetRun } from '@/composables/useRun'

const router = useRouter()
resetRun()
const draft = reactive({ name: '', concept: '', audience: '', question: '', context: '' })

function continueSetup() {
  sessionStorage.setItem('snorkel.projectDraft.v1', JSON.stringify({ ...draft, createdAt: new Date().toISOString() }))
  router.push('/connect')
}
</script>

<style scoped>
.new-project { max-width:900px;margin:0 auto;display:grid;grid-template-columns:280px 1fr;gap:24px; }.intro { padding:24px;background:linear-gradient(150deg,#1a1f30,#34406a);border-radius:14px;color:white;align-self:start; }.intro span { color:#9eacd7;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.12em; }.intro h2 { font-size:26px;margin:8px 0 10px; }.intro p { color:#cbd2e6;line-height:1.6;font-size:13px; }.builder { background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:24px;display:flex;flex-direction:column;gap:18px; }.builder label { display:flex;flex-direction:column;gap:6px; }.builder label>span { font-size:11px;font-weight:700;color:var(--text-2); }.builder input,.builder textarea { border:1px solid var(--border-2);border-radius:8px;padding:10px 12px;color:var(--ink);background:var(--bg);resize:vertical;outline:none; }.builder input:focus,.builder textarea:focus { border-color:var(--accent);background:white; }.two-col { display:grid;grid-template-columns:1fr 1fr;gap:14px; }.next-steps { padding:14px;background:var(--accent-light);border-radius:10px;display:grid;grid-template-columns:1fr 1fr;gap:9px;font-size:11px;color:var(--text-2); }.next-steps strong { grid-column:1/-1;color:var(--ink); }.next-steps div { display:flex;align-items:center;gap:7px; }.next-steps span { width:18px;height:18px;border-radius:50%;background:var(--accent);color:white;display:grid;place-items:center;font-size:9px; }.actions { display:flex;justify-content:space-between;align-items:center;padding-top:4px; }.actions>a { color:var(--text-3);font-size:12px; }
</style>
