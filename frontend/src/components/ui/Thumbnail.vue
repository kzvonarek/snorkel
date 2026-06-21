<template>
  <div class="thumb" :style="{ background: gradient }">
    <span class="thumb-glyph">{{ glyph }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  color:  { type: String, default: '#4B5FA8' },
  glyph:  { type: String, default: '◈' },
})

const gradient = computed(() =>
  `linear-gradient(135deg, ${props.color}cc, ${props.color}66)`
)
</script>

<style scoped>
.thumb {
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  aspect-ratio: 16/9;
}

.thumb-glyph {
  font-size: 28px;
  color: rgba(255,255,255,0.85);
}
</style>
