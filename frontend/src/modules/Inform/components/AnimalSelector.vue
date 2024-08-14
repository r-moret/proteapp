<script setup lang="ts">
import type { AnimalInfo } from '@/modules/Animal/declarations'
import { ref } from 'vue'
import { useAnimalStore } from '@/store/AnimalStore'
import { storeToRefs } from 'pinia'
import ItemSelector from '@/components/ItemSelector.vue'
import AnimalCard from '@/modules/Animal/components/AnimalCard.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'

const model = defineModel<AnimalInfo>()

const { animalList } = storeToRefs(useAnimalStore())

const selectionDrawerOpen = ref(false)
</script>

<template>
  <section class="flex flex-col gap-3">
    <AnimalCard v-if="model" :animal="model" size="compact" />
    <button
      class="w-full rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
      @click="selectionDrawerOpen = true"
    >
      Seleccionar animal
    </button>

    <BottomDrawer class="bg-base-200" size="medium" v-model="selectionDrawerOpen">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Selecciona un animal</h1>
        <div class="flex flex-col gap-2">
          <ItemSelector
            :items="animalList"
            :model-value="model ? [model] : []"
            :search-fn="(animal) => animal.name"
            :max-selections="1"
            include-search
            @update:model-value="(selected: AnimalInfo[]) => (model = selected[0])"
          >
            <template #item="{ item, isSelected, toggleSelect }">
              <AnimalCard
                :animal="item"
                size="regular"
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
