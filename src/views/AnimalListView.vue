<script setup lang="ts">
import AppHeader from '@/skeleton/AppHeader.vue'
import MultiselectorMenu from '@/components/MultiselectorMenu.vue'
import VerticalAnimalCard from '@/modules/Animal/components/VerticalAnimalCard.vue'
import { ref, watchEffect } from 'vue'
import { storeToRefs } from 'pinia'
import { useAnimalStore } from '@/store/AnimalStore'
import { useRouter } from 'vue-router'
import { useFilters } from '@/composable/useFilters'
import type { ContentFilter, TextFilter } from '@/types'

const router = useRouter()
const { animalList, yardList } = storeToRefs(useAnimalStore())

const filters = ref<{
  yard: ContentFilter
  name: TextFilter
}>({
  yard: { type: 'content', item: [...yardList.value] },
  name: { type: 'text', item: '' }
})

const filteredAnimals = useFilters(animalList, filters)

const yardAnimals = (yard: string) => filteredAnimals.value.filter((animal) => animal.yard == yard)

const navigateAnimal = (id: string) => router.push({ name: 'animal', params: { id } })

watchEffect(() => (filters.value.yard.item = yardList.value))
</script>

<template>
  <main class="flex flex-col">
    <AppHeader left="profile" title="Animales" />
    <div class="overflow-y-scroll">
      <div class="join mb-2 w-full px-4 py-2">
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
  </main>
</template>
