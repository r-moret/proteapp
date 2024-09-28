import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authFetch } from '@/composable/useAuthFetch'

import type { Yard, YardInfo, EditYard, EditYardOrder } from '@/modules/Yard/declarations'
import {
  listYards as listYardApi,
  crudYard as crudYardApi,
  crudYardOrder as crudYardOrderApi
} from '@/modules/Yard/api'

import { YardAdapter, YardInfoAdapter, YardOrderAdapter } from '@/modules/Yard/adapters'

export const useYardStore = defineStore('YardStore', () => {
  const yardList = ref<YardInfo[]>([])
  const yardDetails = ref<Yard>()
  const currentOrder = ref<YardInfo[]>()
  const isLoading = ref(false)

  async function fetchYards() {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${listYardApi}`)
      .then((res) => res.json())
      .then((json) => json.map(YardInfoAdapter))
      .then(
        (json: YardInfo[]) =>
          (yardList.value = json.sort((a, b) =>
            a.name.localeCompare(b.name, undefined, { numeric: true })
          ))
      )

    isLoading.value = false
  }

  async function fetchYard(id: string) {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudYardApi}/${id}`)
      .then((res) => res.json())
      .then(YardAdapter)
      .then((yard) => (yardDetails.value = yard))

    isLoading.value = false
  }

  async function createYard(yard: EditYard) {
    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudYardApi}`, {
      method: 'post',
      body: JSON.stringify(yard),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(async (data) => {
      if (!data.ok) {
        throw Error(`Error backend response: ${await data.json()}`)
      }
    })
    await fetchYards()
  }

  async function deleteYard(yardId: string) {
    if (!yardList.value || !yardList.value.map((yard) => yard.id).includes(yardId)) {
      throw Error(
        'Cannot delete a yard that belongs to a yard different than the one that is loaded'
      )
    }

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudYardApi}/${yardId}`, {
      method: 'delete'
    })
    yardList.value = yardList.value.filter((yard) => yard.id !== yardId)
  }

  async function createOrder(yardOrder: EditYardOrder) {
    const response = await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudYardOrderApi}`, {
      method: 'post',
      body: JSON.stringify(yardOrder),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) throw Error('Unexpected error from backend while creating a new yard order')
  }

  async function fetchCurrentOrder() {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudYardOrderApi}/current`)
      .then((res) => {
        if (res.status === 204) throw Error("There's no current order")
        return res.json()
      })
      .then(YardOrderAdapter)
      .then((order) => (currentOrder.value = order.yardOrder))
      .catch(() => (currentOrder.value = []))

    isLoading.value = false
  }

  return {
    yardList,
    currentOrder,
    fetchYard,
    fetchYards,
    createYard,
    deleteYard,
    createOrder,
    fetchCurrentOrder
  }
})
