<script setup lang="ts">
import { ref } from 'vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import ButtonWithSubaction from '@/components/ButtonWithSubaction.vue'
import AnimalFiltersMenu from '@/modules/Animal/components/AnimalFiltersMenu.vue'
import type { AnimalFilters } from '@/types'

const props = defineProps<{
  modelValue: AnimalFilters
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', payload: AnimalFilters): void
}>()

const filtersMenuOpen = ref(false)
</script>

<template>
  <ButtonWithSubaction :show-subaction="false">
    <template #main-button>
      <button
        class="flex h-12 items-center justify-center gap-2 rounded-3xl bg-secondary px-8 text-base font-semibold text-white drop-shadow-2xl"
        @click="filtersMenuOpen = true"
      >
        <span class="i-mingcute-filter-2-fill text-lg" />
        Filtrar
      </button>
    </template>
    <template #subaction-button>
      <button
        class="btn btn-circle btn-outline btn-sm flex flex-nowrap justify-center bg-blue-200 text-blue-500"
      >
        <span class="i-mingcute-add-fill rotate-45 text-xl" />
      </button>
    </template>
  </ButtonWithSubaction>

  <BottomDrawer class="bg-base-200" v-model="filtersMenuOpen">
    <AnimalFiltersMenu
      :model-value="props.modelValue"
      @update:model-value="(event) => emit('update:modelValue', event)"
    />
  </BottomDrawer>
</template>
