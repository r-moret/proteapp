<script setup lang="ts" generic="T extends ObjectWithId">
import type { ObjectWithId } from '@/types'

const props = defineProps<{
  items: T[]
  modelValue: T[]
}>()

const emit = defineEmits<{
  (e: 'update:model-value', payload: T[]): void
}>()

function toggleSelect(item: T) {
  if (props.modelValue.includes(item)) {
    emit(
      'update:model-value',
      props.modelValue.filter((selected) => selected.id !== item.id)
    )
  } else {
    emit('update:model-value', [...props.modelValue, item])
  }
}
</script>

<template>
  <slot
    v-for="item in props.items"
    name="item"
    :key="item.id"
    :toggleSelect
    :isSelected="props.modelValue.includes(item)"
    :item
  />
</template>
