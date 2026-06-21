<template>
  <button class="btn" :class="[`btn--${variant}`, { 'btn--pill': pill }]" v-bind="$attrs">
    <slot />
  </button>
</template>

<script setup>
defineProps({
  variant: { type: String, default: 'primary' }, // primary | secondary | ghost
  pill:    { type: Boolean, default: false },
})
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 8px;
  transition: background 0.12s, color 0.12s, border-color 0.12s;
  white-space: nowrap;
}

.btn--pill { border-radius: var(--radius-pill); }

.btn--primary {
  background: var(--accent);
  color: #fff;
}
.btn--primary:hover { background: var(--accent-hover); }

.btn--secondary {
  background: transparent;
  color: var(--accent);
  border: 1.5px solid var(--accent);
}
.btn--secondary:hover { background: var(--accent-light); }

.btn--ghost {
  background: transparent;
  color: var(--text-2);
  border: 1.5px solid var(--border);
}
.btn--ghost:hover { background: var(--bg); color: var(--ink); }
</style>
