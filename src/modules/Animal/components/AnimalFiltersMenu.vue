<script setup lang="ts">
import BottomDrawer from '@/components/BottomDrawer.vue'
import MultiselectorMenu from '@/components/MultiselectorMenu.vue'
import ButtonWithSubaction from '@/components/ButtonWithSubaction.vue'
import type { ContentFilter } from '@/types'

const props = defineProps<{
  yardOptions: string[]
}>()

const currentFilters = defineModel<{
  yard: ContentFilter
}>('filters', { required: true })
</script>

<template>
  <BottomDrawer class="bg-base-200">
    <template #button="{ open: openDrawer }">
      <ButtonWithSubaction
        :show-subaction="![0, props.yardOptions.length].includes(currentFilters.yard.item.length)"
      >
        <template #main-button>
          <button
            class="flex h-12 items-center justify-center gap-2 rounded-3xl bg-secondary px-8 text-base font-semibold text-white drop-shadow-2xl"
            @click="openDrawer"
          >
            <span class="i-mingcute-filter-2-fill text-lg" />
            Filtrar
          </button>
        </template>
        <template #subaction-button>
          <button
            @click="currentFilters.yard.item = [...props.yardOptions]"
            class="btn btn-circle btn-outline btn-sm flex flex-nowrap justify-center bg-blue-200 text-blue-500"
          >
            <span class="i-mingcute-add-fill rotate-45 text-xl" />
          </button>
        </template>
      </ButtonWithSubaction>
    </template>

    <template #drawer>
      <MultiselectorMenu :options="props.yardOptions" v-model:checked="currentFilters.yard.item" />
    </template>
  </BottomDrawer>
</template>
