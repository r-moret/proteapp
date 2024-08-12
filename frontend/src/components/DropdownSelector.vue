<script setup lang="ts" generic="T">
import TextInput from '@/components/TextInput.vue'
import { uniqueId } from 'lodash'
import { ref, computed, type Ref } from 'vue'
import { onClickOutside } from '@vueuse/core'

const props = withDefaults(
  defineProps<{
    items: T[]
    includeSearch?: boolean
    searchFn?: (item: T) => string
    contentSize?: string
  }>(),
  {
    includeSearch: false,
    searchFn: (item: T) => String(item),
    contentSize: 'w-52'
  }
)

const emit = defineEmits<{
  select: [payload: T]
}>()

const dropdownContent = ref(null)
const searchFilter = ref('')
const identifiedItems = ref(props.items.map((item) => ({ id: uniqueId(), item }))) as Ref<
  { id: string; item: T }[]
>

const searchResults = computed(() => {
  return identifiedItems.value.filter((idItem) =>
    props.searchFn(idItem.item).toLowerCase().includes(searchFilter.value.toLowerCase())
  )
})

function handleSelect(item: T) {
  emit('select', item)
}

onClickOutside(dropdownContent, () => (searchFilter.value = ''))
</script>

<template>
  <div class="dropdown">
    <div tabindex="0" role="button">
      <slot name="button" />
    </div>
    <div class="dropdown-content z-[1]" ref="dropdownContent">
      <ul tabindex="0" :class="['rounded-xl bg-base-100 p-2 shadow', props.contentSize]">
        <li v-if="props.includeSearch">
          <TextInput v-model="searchFilter" name="search-item-input" placeholder="Buscar..." />
          <div class="divider m-0 px-2" />
        </li>
        <li v-for="{ id, item } in searchResults" :key="id">
          <slot name="item" :item :handleSelect="() => handleSelect(item)">
            <button class="w-full truncate px-4 py-3 text-start" @click="handleSelect(item)">
              {{ item }}
            </button>
          </slot>
        </li>
        <li v-if="!searchResults.length">
          <slot name="empty">
            <p class="p-3 text-center italic text-gray-400">No hay resultados</p>
          </slot>
        </li>
      </ul>
    </div>
  </div>
</template>
