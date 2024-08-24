<script setup lang="ts" generic="T extends ObjectWithId">
import type { ObjectWithId } from '@/types'
import TextInput from './TextInput.vue'
import { computed, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    items: T[]
    modelValue: T[]
    includeSearch?: boolean
    searchFn?: (item: T) => string
    maxSelections?: number
  }>(),
  {
    includeSearch: false,
    searchFn: (item: T) => item.id,
    maxSelections: undefined
  }
)

const emit = defineEmits<{
  (e: 'update:model-value', payload: T[]): void
}>()

const searchFilter = ref('')

const searchResults = computed(() => {
  return props.items.filter((item) =>
    props.searchFn(item).toLowerCase().includes(searchFilter.value.toLowerCase())
  )
})

function toggleSelect(item: T) {
  if (props.modelValue.map((item) => item.id).includes(item.id)) {
    emit(
      'update:model-value',
      props.modelValue.filter((selected) => selected.id !== item.id)
    )
  } else if (!props.maxSelections || props.maxSelections > props.modelValue.length) {
    emit('update:model-value', [...props.modelValue, item])
  }
}
</script>

<template>
  <template v-if="props.includeSearch">
    <TextInput v-model="searchFilter" placeholder="Buscar...">
      <template #icon><span class="i-mingcute-search-3-line text-2xl text-secondary" /></template>
    </TextInput>
    <div class="divider m-0" />
  </template>
  <ul class="flex flex-col gap-2">
    <slot
      v-for="item in searchResults"
      name="item"
      :key="item.id"
      :toggleSelect
      :isSelected="props.modelValue.map((item) => item.id).includes(item.id)"
      :item
    />
  </ul>
</template>
