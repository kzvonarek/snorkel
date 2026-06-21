<template>
  <div class="bubble-wrap" :class="role === 'user' ? 'bubble-wrap--user' : 'bubble-wrap--bot'">
    <div v-if="role === 'bot'" class="bubble-avatar">AI</div>
    <div class="bubble" :class="`bubble--${role}`">
      <div class="bubble-text">{{ text }}</div>
      <div class="bubble-time">{{ time }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  role: { type: String, default: 'bot' },  // 'user' | 'bot'
  text: { type: String, required: true },
  time: { type: String, default: '' },
})
</script>

<style scoped>
.bubble-wrap {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  max-width: 85%;
}

.bubble-wrap--user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.bubble-wrap--bot {
  align-self: flex-start;
}

.bubble-avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 9px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.bubble {
  padding: 10px 14px;
  border-radius: 14px;
  max-width: 100%;
}

.bubble--user {
  background: var(--accent);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.bubble--bot {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--ink);
  border-bottom-left-radius: 4px;
}

.bubble-text {
  font-size: 13px;
  line-height: 1.5;
}

.bubble-time {
  font-size: 10px;
  margin-top: 4px;
  opacity: 0.55;
  text-align: right;
}
</style>
