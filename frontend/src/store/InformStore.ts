import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { EditInform, Inform, InformInfo } from '@/modules/Inform/declarations'
import { listInform as listInformApi, crudInform as crudInformApi } from '@/modules/Inform/api'
import { InformAdapter, InformInfoAdapter } from '@/modules/Inform/adapters'
import { authFetch } from '@/composable/useAuthFetch'

export const useInformStore = defineStore('InformStore', () => {
  const informList = ref<InformInfo[]>([])
  const informDetails = ref<Inform>()
  const isLoading = ref(false)

  async function fetchInforms() {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${listInformApi}`)
      .then((res) => res.json())
      .then((json) => json.map(InformInfoAdapter))
      .then((informs) => (informList.value = informs))

    isLoading.value = false
  }

  async function fetchInform(id: string) {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudInformApi}/${id}`)
      .then((res) => res.json())
      .then(InformAdapter)
      .then((inform) => (informDetails.value = inform))

    isLoading.value = false
  }

  async function createInform(inform: EditInform) {
    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudInformApi}`, {
      method: 'post',
      body: JSON.stringify(inform),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    await fetchInforms()
  }

  async function deleteInform(informId: string) {
    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudInformApi}/${informId}`, {
      method: 'delete'
    })

    await fetchInforms()
  }

  return {
    informList,
    informDetails,
    isLoading,

    fetchInforms,
    fetchInform,
    createInform,
    deleteInform
  }
})
