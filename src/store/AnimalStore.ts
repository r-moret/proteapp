import { ref } from 'vue'
import { defineStore } from 'pinia'
import { sleep } from '@/utils'
import type { Animal } from '@/types'
import { fakeAnimals, fakeYards } from '@/fakes'

export const useAnimalStore = defineStore('AnimalStore', () => {
  const animalList = ref<Animal[]>([])
  const yardList = ref<string[]>([])
  const isLoading = ref(false)

  async function fetchAnimals() {
    isLoading.value = true

    await sleep(3000)
    animalList.value = fakeAnimals
    yardList.value = fakeYards
    isLoading.value = false
  }

  const getAnimal = (id: string): Animal | undefined => {
    const results = animalList.value.filter((animal) => animal.id == id)
    return results[0]
  }

  return {
    animalList,
    yardList,
    isLoading,
    fetchAnimals,
    getAnimal
  }
})
