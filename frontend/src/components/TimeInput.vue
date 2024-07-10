<script setup lang="ts">
import { ref } from 'vue'

const TimeUnit = {
  s: { label: 'Segundos', multiplier: 1 },
  min: { label: 'Minutos', multiplier: 60 },
  h: { label: 'Horas', multiplier: 3600 },
  d: { label: 'Días', multiplier: 86400 }
}

const props = withDefaults(
  defineProps<{
    modelValue?: number
    name: string
    timeSize?: 'small' | 'big'
    units?: (keyof typeof TimeUnit)[]
  }>(),
  {
    timeSize: 'small',
    units: () => ['d', 'h', 'min', 's']
  }
)

const emit = defineEmits<{
  'update:model-value': [payload: number]
}>()

const unit = ref<keyof typeof TimeUnit>(props.units[0])
const time = ref(Math.floor((props.modelValue ?? 0) / TimeUnit[unit.value].multiplier))

function handleModification() {
  emit('update:model-value', time.value * TimeUnit[unit.value].multiplier)
}
</script>

<template>
  <div class="mb-4 mt-2 flex h-12 flex-row gap-2">
    <input
      type="number"
      step="1"
      :name="`${props.name}-time`"
      :id="`${props.name}-time`"
      :class="['h-full rounded-lg px-4', props.timeSize === 'small' ? 'w-16' : 'w-24']"
      v-model="time"
      @input="handleModification"
    />

    <select
      :name="`${props.name}-unit`"
      :id="`${props.name}-unit`"
      class="select"
      v-model="unit"
      @change="handleModification"
    >
      <option v-for="unit in props.units" :value="unit" :key="unit">
        {{ TimeUnit[unit].label }}
      </option>
    </select>
  </div>
</template>
