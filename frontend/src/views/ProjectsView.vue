<template>
  <div class="projects">
    <div class="filter-bar">
      <button
        v-for="f in filters"
        :key="f"
        class="filter-btn"
        :class="{ active: activeFilter === f }"
        @click="activeFilter = f"
      >{{ f }}</button>
    </div>

    <div class="project-grid">
      <router-link
        v-for="p in filtered"
        :key="p.id"
        to="/results"
        class="project-card"
      >
        <Thumbnail :color="p.color" :glyph="p.glyph" />
        <div class="card-body">
          <div class="card-name">{{ p.name }}</div>
          <div class="card-meta">
            <StatusBadge :label="p.status" :variant="badgeVariant(p.status)" />
            <span class="card-run">{{ p.lastRun }}</span>
          </div>
          <div v-if="p.pmfScore" class="card-score">
            <span class="score-num">{{ p.pmfScore }}</span>
            <span class="score-label">PMF</span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Thumbnail from '@/components/ui/Thumbnail.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { projects } from '@/data/projects.js'
import { listSimulations } from '@/api/simulation.js'
import { listReports } from '@/api/report.js'

const filters = ['All', 'Ready', 'Running', 'Drafts']
const activeFilter = ref('All')
const liveProjects = ref([])

const filtered = computed(() => {
  const source = liveProjects.value.length ? liveProjects.value : projects
  if (activeFilter.value === 'All') return source
  const map = { Ready: 'Ready', Running: 'Running', Drafts: 'Draft' }
  return source.filter(p => p.status === map[activeFilter.value])
})

function badgeVariant(status) {
  if (status === 'Ready')   return 'ready'
  if (status === 'Running') return 'running'
  return 'draft'
}

function mapSimulation(simulation) {
  const status = simulation.status || 'Draft'
  return {
    id: simulation.simulation_id,
    name: simulation.name || simulation.project_name || simulation.simulation_id,
    status: status === 'ready' ? 'Ready' : status === 'running' ? 'Running' : 'Draft',
    lastRun: simulation.updated_at || simulation.created_at || 'Recently',
    color: '#4B5FA8',
    glyph: '◉',
    pmfScore: simulation.pmf_score || null,
  }
}

function mapReport(report) {
  return {
    id: report.report_id,
    name: report.title || report.report_id,
    status: 'Ready',
    lastRun: report.created_at || 'Recently',
    color: '#3B7355',
    glyph: '▤',
    pmfScore: report.pmf_score || null,
  }
}

onMounted(async () => {
  try {
    const [simulationsRes, reportsRes] = await Promise.all([
      listSimulations(),
      listReports(),
    ])

    const simulations = Array.isArray(simulationsRes?.data) ? simulationsRes.data : simulationsRes?.data?.data || []
    const reports = Array.isArray(reportsRes?.data) ? reportsRes.data : reportsRes?.data?.data || []

    liveProjects.value = [
      ...simulations.map(mapSimulation),
      ...reports.map(mapReport),
    ]
  } catch (error) {
    liveProjects.value = []
  }
})
</script>

<style scoped>
.projects { display: flex; flex-direction: column; gap: 20px; }

.filter-bar { display: flex; gap: 6px; }

.filter-btn {
  padding: 6px 14px;
  border-radius: var(--radius-pill);
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-2);
  border: 1.5px solid var(--border);
  background: var(--surface);
  cursor: pointer;
  transition: background 0.12s, color 0.12s, border-color 0.12s;
}
.filter-btn.active,
.filter-btn:hover {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.project-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  cursor: pointer;
  transition: box-shadow 0.15s, transform 0.15s;
  text-decoration: none;
}
.project-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.card-name { font-size: 13.5px; font-weight: 700; color: var(--ink); margin-bottom: 4px; }

.card-meta { display: flex; align-items: center; gap: 8px; }
.card-run  { font-size: 11px; color: var(--text-3); }

.card-score { display: flex; align-items: baseline; gap: 4px; margin-top: 4px; }
.score-num  { font-family: 'Newsreader', serif; font-size: 28px; font-weight: 600; color: var(--accent); }
.score-label { font-size: 11px; font-weight: 700; color: var(--text-3); }
</style>
