import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { Animal, Yard } from '@/types'
import { listAnimal as listAnimalApi, listYards as listYardApi } from '@/modules/Animal/api'

export const useAnimalStore = defineStore('AnimalStore', () => {
  const animalList = ref<Animal[]>([])
  const yardList = ref<string[]>([])
  const isLoading = ref(false)

  async function fetchAnimals() {
    isLoading.value = true

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${listAnimalApi}`)
      .then((res) => res.json())
      .then((json) => (animalList.value = json))

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${listYardApi}`)
      .then((res) => res.json())
      .then((json: Yard[]) => (yardList.value = json.map((yard) => yard.name)))

    isLoading.value = false
  }

  const getAnimal = computed(() => (id: string): Animal | undefined => {
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
