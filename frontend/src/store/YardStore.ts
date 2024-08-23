import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authFetch } from '@/composable/useAuthFetch'

import type {
  Yard,
  YardInfo,
  EditYard,
  EditYardOrder,
  YardOrder
} from '@/modules/Yard/declarations'
import {
  listYards as listYardApi,
  crudYard as crudYardApi,
  crudYardOrder as crudYardOrderApi,
  listYardsOrder as listYardOrderApi
} from '@/modules/Yard/api'

import { YardAdapter, YardOrderAdapter } from '@/modules/Yard/adapters'

export const useYardStore = defineStore('YardStore', () => {
  const yardList = ref<Yard[]>([])
  const lastYardOrder = ref<YardInfo[]>()
  const yardDetails = ref<Yard>()
  const isLoading = ref(false)

  async function fetchYards() {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${listYardApi}`)
      .then((res) => res.json())
      .then((json: Yard[]) => (yardList.value = json))

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

  async function postYardOrder(yardOrder: EditYardOrder) {
    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudYardOrderApi}`, {
      method: 'post',
      body: JSON.stringify(yardOrder),
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  async function fetchLastYardOrder() {
    isLoading.value = true

    const response = await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${listYardOrderApi}`)
    const json = await response.json()
    const yardOrderList: YardOrder[] = json.map(YardOrderAdapter)

    const mostRecentOrder = yardOrderList.reduce(
      (latest, current) => {
        if (!latest) return current

        return current.date > latest.date ? current : latest
      },
      undefined as YardOrder | undefined
    )

    lastYardOrder.value = mostRecentOrder?.yardOrder

    isLoading.value = false
  }

  return {
    deleteYard,
    createYard,
    yardList,
    fetchYards,
    postYardOrder,
    fetchLastYardOrder,
    lastYardOrder,
    fetchYard
  }
})
