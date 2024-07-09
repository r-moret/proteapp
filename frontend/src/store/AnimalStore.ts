import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { Animal, Yard } from '@/modules/Animal/declarations'
import { listAnimal as listAnimalApi, listYards as listYardApi } from '@/modules/Animal/api'
import { AnimalAdapter } from '@/modules/Animal/adapters'

export const useAnimalStore = defineStore('AnimalStore', () => {
  const animalList = ref<Animal[]>([])
  const yardList = ref<string[]>([])
  const isLoading = ref(false)

  async function fetchAnimals() {
    isLoading.value = true

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${listAnimalApi}`)
      .then((res) => res.json())
      .then((json) => json.map(AnimalAdapter))
      .then((animals) => (animalList.value = animals))

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${listYardApi}`)
      .then((res) => res.json())
      .then((json: Yard[]) => (yardList.value = json.map((yard) => yard.name)))

    isLoading.value = false
  }

  const getAnimal = computed(() => (id: number): Animal | undefined => {
    return animalList.value.find((animal) => animal.id == id)
  })

  return {
    animalList,
    yardList,
    isLoading,
    fetchAnimals,
    getAnimal
  }
})
