<template>
  <div class="shell">
    <Sidebar />
    <div class="shell-main">
      <TopBar :title="topbarTitle" :action="topbarAction" @action="handleAction" />
      <main class="shell-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/layout/Sidebar.vue'
import TopBar from '@/components/layout/TopBar.vue'

const route = useRoute()
const router = useRouter()

const routeMeta = {
  '/':          { title: 'Overview',           action: '' },
  '/projects':  { title: 'Projects',           action: 'New project' },
  '/connect':   { title: 'Connect data',        action: 'Save connections' },
  '/personas':  { title: 'Personas & segments', action: 'Add persona' },
  '/market':    { title: 'Market context',       action: 'Save' },
  '/products':  { title: 'Product material',     action: 'Upload asset' },
  '/sandbox':   { title: 'Configure run',        action: 'Run simulation' },
  '/swarm':     { title: 'Live swarm feed',      action: '' },
  '/results':   { title: 'Results dashboard',    action: 'Build report →' },
  '/report':    { title: 'Report & chat',        action: 'Download PDF' },
}

const topbarTitle  = computed(() => routeMeta[route.path]?.title  ?? '')
const topbarAction = computed(() => routeMeta[route.path]?.action ?? '')

const actionRoutes = {
  '/results': '/report',
  '/sandbox': '/swarm',
}

function handleAction() {
  const next = actionRoutes[route.path]
  if (next) router.push(next)
}
</script>

<style scoped>
.shell {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.shell-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.shell-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--content-py) var(--content-px);
  background: var(--bg);
}
</style>
