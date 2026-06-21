<template>
  <aside class="sidebar">
    <div class="sidebar-logo">
      <span class="logo-mark">PMF</span>
      <span class="logo-word">Studio</span>
    </div>

    <nav class="sidebar-nav">
      <div v-for="group in navGroups" :key="group.label" class="nav-group">
        <div class="nav-group-label">{{ group.label }}</div>
        <router-link
          v-for="item in group.items"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          :class="{ active: $route.path === item.to }"
        >
          <span class="nav-icon" v-html="item.icon"></span>
          <span>{{ item.label }}</span>
          <span v-if="item.live && runState.isRunning" class="live-badge">live</span>
        </router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="user-avatar">BT</div>
      <div class="user-info">
        <div class="user-name">Brandon Tran</div>
        <div class="user-role">Researcher</div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import runState from '@/composables/useRun.js'

const navGroups = [
  {
    label: 'Workspace',
    items: [
      { to: '/',         label: 'Overview',         icon: '⬡' },
      { to: '/projects', label: 'Projects',          icon: '▦' },
    ]
  },
  {
    label: 'Build study',
    items: [
      { to: '/connect',  label: 'Connect data',      icon: '⇌' },
      { to: '/personas', label: 'Personas',           icon: '◎' },
      { to: '/market',   label: 'Market context',     icon: '◈' },
      { to: '/products', label: 'Product material',   icon: '⬕' },
    ]
  },
  {
    label: 'Simulate',
    items: [
      { to: '/sandbox',  label: 'Configure run',      icon: '⧉' },
      { to: '/swarm',    label: 'Live feed',           icon: '◉', live: true },
    ]
  },
  {
    label: 'Output',
    items: [
      { to: '/results',  label: 'Results',             icon: '◫' },
      { to: '/report',   label: 'Report & chat',       icon: '▤' },
    ]
  },
]
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-w);
  min-height: 100vh;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-logo {
  height: var(--topbar-h);
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 18px;
  border-bottom: 1px solid var(--border);
}

.logo-mark {
  font-weight: 700;
  font-size: 13px;
  background: var(--accent);
  color: #fff;
  padding: 3px 7px;
  border-radius: 6px;
  letter-spacing: 0.05em;
}

.logo-word {
  font-weight: 600;
  font-size: 14px;
  color: var(--ink);
}

.sidebar-nav {
  flex: 1;
  padding: 14px 10px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.nav-group-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-3);
  padding: 0 8px;
  margin-bottom: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 8px;
  border-radius: 8px;
  font-size: 13.5px;
  font-weight: 500;
  color: var(--text-2);
  transition: background 0.12s, color 0.12s;
  cursor: pointer;
}

.nav-item:hover {
  background: rgba(75, 95, 168, 0.08);
  color: var(--accent);
}

.nav-item.active {
  background: var(--accent);
  color: #fff;
}

.nav-icon {
  font-size: 15px;
  width: 18px;
  text-align: center;
  flex-shrink: 0;
}

.live-badge {
  margin-left: auto;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  background: #e53935;
  color: #fff;
  padding: 2px 6px;
  border-radius: 10px;
  animation: pulse 1.4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}

.sidebar-footer {
  padding: 12px 14px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-name {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--ink);
}

.user-role {
  font-size: 11px;
  color: var(--text-3);
}
</style>
