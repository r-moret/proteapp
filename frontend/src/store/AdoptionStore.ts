import { ref } from 'vue'
import { defineStore } from 'pinia'
import type {
  AdoptionInfo,
  Adoption,
  EditMonitoring,
  EditAdoption
} from '@/modules/Adoption/declarations'
import type { Animal } from '@/modules/Animal/declarations'
import {
  crudAdoption as crudAdoptionApi,
  listAdoptions as listAdoptionsApi,
  crudMonitoring as crudMonitoringApi
} from '@/modules/Adoption/api'

import { AdoptionInfoAdapter, AdoptionAdapter } from '@/modules/Adoption/adapters'

export const useAdoptionStore = defineStore('AdoptionStore', () => {
  const adoptionList = ref<AdoptionInfo[]>([])
  const adoptionDetails = ref<Adoption>()
  const animalDetails = ref<Animal>()
  const isLoading = ref(false)

  async function fetchAdoptions(kind: string) {
    isLoading.value = true
    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${listAdoptionsApi}`)
      .then((res) => res.json())
      .then((json) => json.map(AdoptionInfoAdapter))
      .then((adoption) => (adoptionList.value = adoption))

    isLoading.value = false
    adoptionList.value = adoptionList.value.filter((adoption) => adoption.kind === kind)
  }

  async function deleteAdoption(adoptionId: string) {
    if (
      !adoptionList.value ||
      !adoptionList.value.map((adoption) => adoption.id).includes(adoptionId)
    ) {
      throw Error(
        'Cannot delete an adoption that belongs to an adoption different than the one that is loaded'
      )
    }

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAdoptionApi}/${adoptionId}`, {
      method: 'delete'
    })
    adoptionList.value = adoptionList.value.filter((adoption) => adoption.id !== adoptionId)
  }

  async function fetchAdoption(id: string) {
    isLoading.value = true

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAdoptionApi}/${id}`)
      .then((res) => res.json())
      .then(AdoptionAdapter)
      .then((adoption) => (adoptionDetails.value = adoption))

    isLoading.value = false
  }

  async function createAdoption(adoption: EditAdoption) {
    if (
      !adoptionDetails.value ||
      !animalDetails.value ||
      adoption.animal !== animalDetails.value.id
    ) {
      throw Error('Cannot create an adoption for an animal different than the one that is loaded')
    }

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAdoptionApi}`, {
      method: 'post',
      body: JSON.stringify(adoption),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(async (data) => {
      if (!data.ok) {
        throw Error(`Error backend response: ${await data.json()}`)
      }
    })

    await fetchAdoption(adoptionDetails.value.id)
  }

  async function createMonitoring(monitoring: EditMonitoring) {
    if (!adoptionDetails.value || monitoring.adoption !== adoptionDetails.value.id) {
      throw Error(
        'Cannot create an monitoring for an adoption different than the one that is loaded'
      )
    }

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudMonitoringApi}`, {
      method: 'post',
      body: JSON.stringify(monitoring),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(async (data) => {
      if (!data.ok) {
        throw Error(`Error backend response: ${await data.json()}`)
      }
    })

    // INFO: Improvement point, same as treatment
    await fetchAdoption(adoptionDetails.value.id)
  }

  async function deleteMonitoring(monitoringId: string) {
    if (
      !adoptionDetails.value ||
      !adoptionDetails.value.monitorings.map((monitoring) => monitoring.id).includes(monitoringId)
    ) {
      throw Error(
        'Cannot delete an monitoring that belongs to an adoption different than the one that is loaded'
      )
    }

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudMonitoringApi}/${monitoringId}`, {
      method: 'delete'
    })

    adoptionDetails.value.monitorings = adoptionDetails.value.monitorings.filter(
      (monitoring) => monitoring.id !== monitoringId
    )
  }

  return {
    fetchAdoptions,
    adoptionList,
    adoptionDetails,
    fetchAdoption,
    deleteAdoption,
    isLoading,
    deleteMonitoring,
    createMonitoring,
    createAdoption
  }
})
