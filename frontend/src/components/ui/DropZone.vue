<template>
  <div
    class="dropzone"
    :class="{ 'dropzone--over': over }"
    @dragover.prevent="over = true"
    @dragleave="over = false"
    @drop.prevent="onDrop"
    @click="$refs.input.click()"
  >
    <div class="dropzone-icon">⬆</div>
    <div class="dropzone-text">{{ label }}</div>
    <div class="dropzone-sub">{{ sub }}</div>
    <input ref="input" type="file" multiple style="display:none" @change="onSelect" />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  label: { type: String, default: 'Drop files here or click to browse' },
  sub:   { type: String, default: 'PDF, DOCX, PNG, CSV accepted' },
})
const emit = defineEmits(['files'])

const over = ref(false)

function onDrop(e) {
  over.value = false
  emit('files', [...e.dataTransfer.files])
}

function onSelect(e) {
  emit('files', [...e.target.files])
}
</script>

<style scoped>
.dropzone {
  border: 2px dashed var(--border-2);
  border-radius: var(--radius-card);
  padding: 36px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
  background: var(--surface);
}

.dropzone:hover,
.dropzone--over {
  border-color: var(--accent);
  background: var(--accent-light);
}

.dropzone-icon {
  font-size: 22px;
  color: var(--text-3);
}

.dropzone-text {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--ink);
}

.dropzone-sub {
  font-size: 12px;
  color: var(--text-3);
}
</style>
