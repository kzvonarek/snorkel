<template>
  <header class="topbar">
    <div class="topbar-title">{{ title }}</div>
    <div class="topbar-actions">
      <button v-if="action" class="action-btn" @click="$emit('action')">
        {{ action }}
      </button>
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: { type: String, default: '' },
  action: { type: String, default: '' },
})
defineEmits(['action'])
</script>

<style scoped>
.topbar {
  height: var(--topbar-h);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 var(--content-px);
  background: var(--surface);
  gap: 16px;
}

.topbar-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  flex: 1;
}

.action-btn {
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  background: var(--accent);
  padding: 7px 16px;
  border-radius: var(--radius-pill);
  transition: background 0.12s;
}

.action-btn:hover {
  background: var(--accent-hover);
}
</style>
