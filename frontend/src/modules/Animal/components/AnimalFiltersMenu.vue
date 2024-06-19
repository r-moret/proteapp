<script setup lang="ts">
import SelectorMenu from '@/components/SelectorMenu.vue'
import type { AnimalFilters } from '@/types'
import { filterLabels } from '../animal.config'

const props = defineProps<{
  modelValue: AnimalFilters
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', payload: AnimalFilters): void
}>()

const updateAgeFilter = (extreme: 'max' | 'min', event: Event) => {
  const newValue = (event.target as HTMLInputElement).value

  emit('update:modelValue', {
    ...props.modelValue,
    age: { ...props.modelValue.age, [extreme]: newValue }
  })
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <h1 class="text-3xl font-semibold">Filtros</h1>
    <div class="flex flex-col gap-4">
      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Patios</h2>
        <SelectorMenu
          :include-all-control="true"
          :model-value="props.modelValue.yards"
          @update:model-value="
            (event) => emit('update:modelValue', { ...props.modelValue, yards: event })
          "
        />
      </div>
      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Edad</h2>
        <div class="flex gap-4">
          <span
            >De
            <input
              type="number"
              placeholder="0"
              class="input input-sm input-bordered input-secondary w-12"
              :value="props.modelValue.age.min"
              @input="(event) => updateAgeFilter('min', event)"
            />
            a
            <input
              type="number"
              placeholder="30"
              class="input input-sm input-bordered input-secondary w-12"
              :value="props.modelValue.age.max"
              @input="(event) => updateAgeFilter('max', event)"
            />
            años
          </span>
        </div>
      </div>
      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Sexo</h2>
        <SelectorMenu
          :include-all-control="false"
          :model-value="props.modelValue.sex"
          :model-labels="filterLabels.sex"
          @update:model-value="
            (event) => emit('update:modelValue', { ...props.modelValue, sex: event })
          "
        />
      </div>
      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Castración</h2>
        <SelectorMenu
          :include-all-control="false"
          :model-value="props.modelValue.castration"
          :model-labels="filterLabels.castration"
          @update:model-value="
            (event) => emit('update:modelValue', { ...props.modelValue, castration: event })
          "
        />
      </div>
      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Compatibilidad</h2>
        <SelectorMenu
          :include-all-control="false"
          :model-value="props.modelValue.compatible"
          :model-labels="filterLabels.compatible"
          @update:model-value="
            (event) => emit('update:modelValue', { ...props.modelValue, compatible: event })
          "
        />
      </div>
    </div>
  </div>
</template>
