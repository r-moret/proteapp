import { defineStore } from 'pinia'
import type { EditPerson, Person } from '@/modules/Person/declarations'
import { ref } from 'vue'
import { PersonAdapter } from '@/modules/Person/adapters'
import { listPeople as listPeopleApi, crudPerson as crudPersonApi } from '@/modules/Person/api'
import { authFetch } from '@/composable/useAuthFetch'

export const usePersonStore = defineStore('PersonStore', () => {
  const personList = ref<Person[]>([])
  const personDetails = ref<Person>()
  const isLoading = ref(false)

  async function fetchPerson(id: string) {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudPersonApi}/${id}`)
      .then((res) => res.json())
      .then(PersonAdapter)
      .then((person) => (personDetails.value = person))

    isLoading.value = false
  }

  async function fetchPeople() {
    isLoading.value = true
    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${listPeopleApi}`)
      .then((res) => res.json())
      .then((json) => json.map(PersonAdapter))
      .then((person) => (personList.value = person))

    isLoading.value = false
  }

  async function deletePerson(personId: string) {
    if (!personList.value || !personList.value.map((person) => person.id).includes(personId)) {
      throw Error(
        'Cannot delete an person that belongs to an person different than the one that is loaded'
      )
    }

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudPersonApi}/${personId}`, {
      method: 'delete'
    })
    personList.value = personList.value.filter((person) => person.id !== personId)
  }

  async function createPerson(person: EditPerson) {
    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudPersonApi}`, {
      method: 'post',
      body: JSON.stringify(person),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(async (data) => {
      if (!data.ok) {
        throw Error(`Error backend response: ${await data.json()}`)
      }
    })
    await fetchPeople()
  }

  async function updatePerson(personId: string, person: EditPerson) {
    const response = await authFetch(
      `${import.meta.env.VITE_BACKEND_URL}/${crudPersonApi}/${personId}`,
      {
        method: 'put',
        body: JSON.stringify(person),
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) throw Error(`Error backend response: ${await response.json()}`)

    await fetchPeople()
  }

  return {
    personList,
    personDetails,
    fetchPeople,
    deletePerson,
    createPerson,
    fetchPerson,
    updatePerson
  }
})
