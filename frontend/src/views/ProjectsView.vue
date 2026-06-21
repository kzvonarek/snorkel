<template>
  <div class="projects">
    <div class="hero">
      <div><span class="eyebrow">Curated demo studies</span><h2>What do you want to test?</h2><p>Create a PMF simulation from one of three fully prepared concepts.</p></div>
      <BaseButton variant="primary" pill @click="router.push('/projects/new')">New blank project</BaseButton>
    </div>

    <div class="project-grid">
      <button v-for="topic in demoTopics" :key="topic.id" class="project-card" @click="openTopic(topic)">
        <div class="topic-mark" :style="{ background: topic.color }">{{ topic.glyph }}</div>
        <span class="category">{{ topic.category }}</span>
        <h3>{{ topic.name }}</h3>
        <p>{{ topic.tagline }}</p>
        <div class="card-footer"><span>9 personas</span><strong>Start simulation -></strong></div>
      </button>
    </div>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import BaseButton from '@/components/ui/BaseButton.vue'
import { demoTopics } from '@/data/demoTopics'
import { launchDemoTopic } from '@/composables/useRun'

const router = useRouter()
function create(topic) { launchDemoTopic(topic.id); router.push('/swarm') }
function openTopic(topic) { create(topic) }
</script>

<style scoped>
.projects { display:flex;flex-direction:column;gap:24px; }.hero { display:flex;justify-content:space-between;align-items:flex-end;padding:24px 26px;background:linear-gradient(120deg,#1a1f30,#303a62);border-radius:16px;color:#fff; }.hero h2 { font-size:28px;margin:3px 0 5px; }.hero p { color:#c7cee4; }.eyebrow { font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:#9eacd7; }
.project-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:18px; }.project-card { text-align:left;background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:20px;min-height:260px;display:flex;flex-direction:column;align-items:flex-start;transition:.18s; }.project-card:hover { transform:translateY(-3px);box-shadow:var(--shadow-md);border-color:var(--accent); }.topic-mark,.option-glyph { width:48px;height:48px;border-radius:12px;color:white;display:grid;place-items:center;font-weight:800;letter-spacing:.05em; }.category { color:var(--text-3);font-size:11px;text-transform:uppercase;letter-spacing:.08em;margin-top:18px; }.project-card h3 { font-size:22px;margin:5px 0 8px; }.project-card p { color:var(--text-2);line-height:1.55; }.card-footer { margin-top:auto;width:100%;display:flex;justify-content:space-between;padding-top:18px;border-top:1px solid var(--border);font-size:12px;color:var(--text-3); }.card-footer strong { color:var(--accent); }
.modal-backdrop { position:fixed;inset:0;background:rgba(15,20,35,.58);display:grid;place-items:center;z-index:20;padding:20px; }.picker { width:min(680px,100%);background:white;border-radius:16px;padding:24px;box-shadow:0 24px 80px rgba(0,0,0,.25); }.picker-heading { display:flex;justify-content:space-between;margin-bottom:18px; }.picker-heading h2 { margin-top:3px; }.close { color:var(--text-3);font-size:18px; }.picker-option { width:100%;display:grid;grid-template-columns:50px 1fr auto;gap:14px;align-items:center;text-align:left;padding:15px 8px;border-top:1px solid var(--border); }.picker-option:hover { background:var(--bg); }.picker-option span { display:flex;flex-direction:column; }.picker-option small { color:var(--text-3); }.picker-option p { font-size:12px;color:var(--text-2);margin-top:4px; }.picker-option b { color:var(--accent);font-size:12px; }.option-glyph { width:42px;height:42px;border-radius:10px; }
</style>
