<template>
  <div class="connect">
    <div class="fidelity-banner">
      <span class="banner-icon">◎</span>
      <div>
        <div class="banner-title">Data fidelity: <strong>High</strong></div>
        <div class="banner-sub">3 sources connected · 91% average persona match</div>
      </div>
    </div>

    <div v-for="group in connectorGroups" :key="group.category" class="connector-group">
      <div class="group-label">{{ group.category }}</div>
      <div class="connector-list">
        <div v-for="c in group.items" :key="c.id" class="connector-card">
          <div class="conn-icon">{{ c.icon }}</div>
          <div class="conn-info">
            <div class="conn-name">{{ c.name }}</div>
            <div v-if="c.match" class="conn-match">{{ c.match }}% persona match</div>
            <ProgressBar v-if="c.connected" :value="c.progress" style="margin-top:6px;" />
          </div>
          <button
            class="conn-toggle"
            :class="{ connected: c.connected }"
            @click="toggle(c)"
          >{{ c.connected ? 'Connected' : 'Connect' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import { connectorGroups as raw } from '@/data/connectors.js'

const connectorGroups = reactive(JSON.parse(JSON.stringify(raw)))

function toggle(c) {
  c.connected = !c.connected
  c.progress = c.connected ? c.match ?? 50 : 0
}
</script>

<style scoped>
.connect { display: flex; flex-direction: column; gap: 28px; }

.fidelity-banner {
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--success-bg);
  border: 1px solid var(--success-fg);
  border-radius: var(--radius-card);
  padding: 14px 18px;
  color: var(--success-fg);
}
.banner-icon { font-size: 20px; }
.banner-title { font-size: 13.5px; font-weight: 600; }
.banner-sub   { font-size: 12px; opacity: 0.8; margin-top: 2px; }

.group-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 10px;
}

.connector-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.connector-card {
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 16px;
}

.conn-icon { font-size: 20px; flex-shrink: 0; }
.conn-info { flex: 1; }
.conn-name  { font-size: 13.5px; font-weight: 600; color: var(--ink); }
.conn-match { font-size: 11.5px; color: var(--text-3); margin-top: 2px; }

.conn-toggle {
  font-size: 12px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: var(--radius-pill);
  border: 1.5px solid var(--accent);
  color: var(--accent);
  background: transparent;
  cursor: pointer;
  transition: background 0.12s, color 0.12s;
  flex-shrink: 0;
}
.conn-toggle.connected { background: var(--accent); color: #fff; }
</style>
