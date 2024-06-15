import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { fakeTreatments } from '@/fakes'
import { sleep } from '@/utils'
import type { Treatment } from '@/types'

export const useTreatmentStore = defineStore('TreatmentStore', () => {
  const treatmentList = ref<Treatment[]>([])
  const isLoading = ref<boolean>(false)

  const getTreatment = computed(() => (id: string): Treatment | undefined => {
    return treatmentList.value.find((treatment) => treatment.id == id)
  })

  async function fetchTreatments() {
    isLoading.value = true
    await sleep(3000)
    treatmentList.value = fakeTreatments
    isLoading.value = false
  }

  return {
    treatmentList,
    getTreatment,
    fetchTreatments
  }
})
