<script setup lang="ts">
import AppHeader from '@/skeleton/AppHeader.vue'
import MultiselectorMenu from '@/components/MultiselectorMenu.vue'
import AnimalCard from '@/modules/Animal/components/AnimalCard.vue'
import SkeletonAnimalCard from '@/modules/Animal/components/SkeletonAnimalCard.vue'
import { ref, watchEffect } from 'vue'
import { storeToRefs } from 'pinia'
import { useAnimalStore } from '@/store/AnimalStore'
import { useFilters } from '@/composable/useFilters'
import type { ContentFilter, TextFilter } from '@/types'

const { animalList, yardList, isLoading } = storeToRefs(useAnimalStore())

const filters = ref<{
  yard: ContentFilter
  name: TextFilter
}>({
  yard: { type: 'content', item: [...yardList.value] },
  name: { type: 'text', item: '' }
})

const filteredAnimals = useFilters(animalList, filters)

watchEffect(() => (filters.value.yard.item = yardList.value))
</script>

<template>
  <main class="flex flex-col">
    <AppHeader left="profile" title="Animales" />
    <div class="scroll-stable h-0 flex-auto overflow-y-scroll">
      <div class="join w-full px-4 py-2">
        <input
          class="input join-item input-bordered flex-1 focus:outline-none"
          placeholder="Buscar animal"
          v-model="filters.name.item"
        />
        <div class="dropdown dropdown-end dropdown-bottom flex-none">
          <div
            tabindex="0"
            role="button"
            class="btn btn-secondary join-item text-base active:outline"
          >
            Patios
            <span class="i-mingcute-triangle-fill rotate-180 text-sm" />
          </div>
          <div
            tabindex="0"
            class="bg-box dropdown-content z-[1] w-56 rounded-box bg-base-100 p-4 shadow"
          >
            <MultiselectorMenu :options="yardList" v-model:checked="filters.yard.item" />
          </div>
        </div>
      </div>
      <div class="px-6">
        <template v-if="isLoading">
          <div v-for="n in 10" :key="n">
            <SkeletonAnimalCard />
            <div class="divider my-1"></div>
          </div>
        </template>
        <template v-else>
          <div v-for="animal in filteredAnimals" :key="animal.name">
            <AnimalCard class="mx-0 my-0" :animal="animal" />
            <div class="divider my-1"></div>
          </div>
        </template>
      </div>
    </div>
  </main>
</template>
