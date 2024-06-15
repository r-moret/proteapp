<script setup lang="ts">
import { ref, watchEffect } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { omit } from 'lodash'

import AppHeader from '@/skeleton/AppHeader.vue'
import VerticalAnimalCard from '@/modules/Animal/components/VerticalAnimalCard.vue'
import AnimalFiltersMenuButton from '@/modules/Animal/components/AnimalFiltersMenuButton.vue'
import { useAnimalStore } from '@/store/AnimalStore'
import type { AnimalFilters } from '@/types'
import { useAnimalFilters } from '@/modules/Animal/composable/useAnimalFilters'

const router = useRouter()
const { animalList, yardList } = storeToRefs(useAnimalStore())

const searchInput = ref<HTMLElement | null>(null)

const filters = ref<AnimalFilters>({
  name: '',
  yards: yardList.value.reduce((acc, yard) => ({ ...acc, [yard]: true }), {})
})

const filteredAnimals = useAnimalFilters(animalList, filters)

const yardAnimals = (yard: string) => filteredAnimals.value.filter((animal) => animal.yard == yard)

const navigateAnimal = (id: string) => router.push({ name: 'animal', params: { id } })

const updateFilters = (newFilters: AnimalFilters) => {
  filters.value = newFilters
}

watchEffect(() => {
  filters.value.yards = {
    ...filters.value.yards,
    ...omit(
      yardList.value.reduce((acc, yard) => ({ ...acc, [yard]: true }), {}),
      Object.keys(filters.value.yards)
    )
  }
})
</script>

<template>
  <main class="flex flex-col">
    <AppHeader left="profile" title="Animales" />
    <div class="grid flex-grow overflow-y-scroll">
      <div class="col-start-1 row-start-1 overflow-y-scroll">
        <div class="mb-4 mt-2 flex h-12 w-full px-4" @click="searchInput?.focus()">
          <div class="flex items-center justify-center rounded-l-lg bg-white px-3">
            <span class="i-mingcute-search-3-line text-2xl text-secondary" />
          </div>
          <div class="divider divider-horizontal mx-0 w-fit bg-white py-2" />
          <input
            type="text"
            name="animal-search"
            id="animal-search"
            class="h-full w-full rounded-r-lg px-4"
            placeholder="Buscar animal"
            ref="searchInput"
            autocomplete="off"
            v-model="filters.name"
          />
        </div>
        <div class="flex flex-col gap-1 px-0">
          <div v-for="(yard, yardNumber) in yardList" :key="yard" class="flex flex-col px-6">
            <h2 class="text-xl font-semibold">{{ yard }}</h2>
            <div class="carousel w-full gap-4 py-4">
              <VerticalAnimalCard
                v-for="animal in yardAnimals(yard)"
                :key="animal.id"
                :animal="animal"
                class="carousel-item rounded-lg shadow-lg"
                @click="navigateAnimal(animal.id)"
              />
            </div>
            <div v-if="yardNumber != yardList.length - 1" class="divider m-1" />
          </div>
        </div>
      </div>
      <div class="z-10 col-start-1 row-start-1 mb-4 place-self-end justify-self-center">
        <AnimalFiltersMenuButton :model-value="filters" @update:model-value="updateFilters" />
      </div>
    </div>
  </main>
</template>
