import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { AdoptionList } from '@/modules/Animal/declarations'
import { listAdoptions as listAdoptionsApi } from '@/modules/Animal/api'

import { AdoptionListAdapter } from '@/modules/Animal/adapters'

export const useAdoptionStore = defineStore('AdoptionStore', () => {
  const adoptionList = ref<AdoptionList[]>([])
  const isLoading = ref(false)

  async function fetchAdoptions() {
    isLoading.value = true
    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${listAdoptionsApi}`)
      .then((res) => res.json())
      .then((json) => json.map(AdoptionListAdapter))
      .then((adoption) => (adoptionList.value = adoption))
    isLoading.value = false
  }

  return {
    fetchAdoptions,
    adoptionList
  }
})
