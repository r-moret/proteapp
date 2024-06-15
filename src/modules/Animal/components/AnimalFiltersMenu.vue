<script setup lang="ts">
import SelectorMenu from '@/components/SelectorMenu.vue'
import type { AnimalFilters } from '@/types'

const props = defineProps<{
  modelValue: AnimalFilters
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', payload: AnimalFilters): void
}>()
</script>

<template>
  <div class="flex flex-col gap-3">
    <h1 class="text-3xl font-semibold">Filtros</h1>
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
  </div>
</template>
