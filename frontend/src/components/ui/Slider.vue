<template>
  <div class="slider-wrap">
    <div class="slider-header">
      <span class="slider-label">{{ label }}</span>
      <span class="slider-value">{{ modelValue }}</span>
    </div>
    <input
      type="range"
      class="slider-input"
      :min="min"
      :max="max"
      :step="step"
      :value="modelValue"
      @input="$emit('update:modelValue', +$event.target.value)"
    />
    <div class="slider-range">
      <span>{{ min }}</span>
      <span>{{ max }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label:      { type: String, default: '' },
  modelValue: { type: Number, default: 0 },
  min:        { type: Number, default: 0 },
  max:        { type: Number, default: 100 },
  step:       { type: Number, default: 1 },
})
defineEmits(['update:modelValue'])
</script>

<style scoped>
.slider-wrap {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slider-label {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--ink);
}

.slider-value {
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
  min-width: 24px;
  text-align: right;
}

.slider-input {
  width: 100%;
  accent-color: var(--accent);
  height: 4px;
  cursor: pointer;
}

.slider-range {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: var(--text-3);
}
</style>
