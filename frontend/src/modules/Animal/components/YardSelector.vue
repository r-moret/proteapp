<script setup lang="ts">
import type { YardInfo } from '@/modules/Yard/declarations'
import { ref } from 'vue'
import { useYardStore } from '@/store/YardStore'
import { storeToRefs } from 'pinia'
import ItemSelector from '@/components/ItemSelector.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import YardCard from '@/modules/Yard/components/YardCard.vue'

const model = defineModel<YardInfo | null>()

const { yardList } = storeToRefs(useYardStore())

const selectionDrawerOpen = ref(false)
</script>

<template>
  <section class="flex flex-col gap-3">
    <YardCard v-if="model" :yard="model" />
    <button
      class="w-full rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
      @click="selectionDrawerOpen = true"
    >
      Seleccionar patio
    </button>

    <BottomDrawer class="bg-base-200" size="medium" v-model="selectionDrawerOpen">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Selecciona un patio</h1>
        <div class="flex flex-col gap-2">
          <ItemSelector
            :items="yardList"
            :model-value="model ? [model] : []"
            :search-fn="(yard) => yard.name"
            :max-selections="1"
            include-search
            @update:model-value="(selected: YardInfo[]) => (model = selected[0])"
          >
            <template #item="{ item, isSelected, toggleSelect }">
              <YardCard
                :yard="item"
                :class="[
                  'border-2',
                  isSelected ? 'border-secondary shadow-secondary' : 'border-transparent'
                ]"
                @click="toggleSelect(item)"
              />
            </template>
          </ItemSelector>
        </div>
      </div>
    </BottomDrawer>
  </section>
</template>
