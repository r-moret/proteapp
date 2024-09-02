import { ref } from 'vue'
import { defineStore } from 'pinia'
import type {
  Animal,
  AnimalInfo,
  EditAppointment,
  EditTreatment,
  EnrichedEditAnimal
} from '@/modules/Animal/declarations'
import {
  listAnimal as listAnimalApi,
  crudAnimal as crudAnimalApi,
  crudTreatment as crudTreatmentApi,
  crudAppointment as crudAppointmentApi
} from '@/modules/Animal/api'

import { AnimalAdapter, AnimalInfoAdapter, EditAnimalAdapter } from '@/modules/Animal/adapters'
import { authFetch } from '@/composable/useAuthFetch'
import { omit } from 'lodash'

export const useAnimalStore = defineStore('AnimalStore', () => {
  const animalList = ref<AnimalInfo[]>([])
  const animalDetails = ref<Animal>()
  const isLoading = ref(false)

  async function fetchAnimals() {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${listAnimalApi}`)
      .then((res) => res.json())
      .then((json) => json.map(AnimalInfoAdapter))
      .then((animals) => (animalList.value = animals))

    isLoading.value = false
  }

  async function fetchAnimal(id: string) {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAnimalApi}/${id}`)
      .then((res) => res.json())
      .then(AnimalAdapter)
      .then((animal) => (animalDetails.value = animal))

    isLoading.value = false
  }

  async function createAnimal(enrichedAnimal: EnrichedEditAnimal) {
    const animal = EditAnimalAdapter({ ...enrichedAnimal, yard: enrichedAnimal.yard?.id })

    const response = await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAnimalApi}`, {
      method: 'post',
      body: JSON.stringify(omit(animal, 'image')),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) throw Error(`Error backend response: ${await response.json()}`)
    if (!animal.image) return
    const createdAnimal = AnimalAdapter(await response.json())

    const image = await fetch(animal.image)
    const imageFile = await image.blob()

    const body = new FormData()
    body.set('image', imageFile)

    await authFetch(
      `${import.meta.env.VITE_BACKEND_URL}/${crudAnimalApi}/${createdAnimal.id}/image`,
      {
        method: 'post',
        body
      }
    )

    await fetchAnimals()
  }

  async function updateAnimal(animalId: string, enrichedAnimal: EnrichedEditAnimal) {
    const animal = EditAnimalAdapter({ ...enrichedAnimal, yard: enrichedAnimal.yard?.id })

    const response = await authFetch(
      `${import.meta.env.VITE_BACKEND_URL}/${crudAnimalApi}/${animalId}`,
      {
        method: 'put',
        body: JSON.stringify(omit(animal, 'image')),
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) return // TODO error
    if (animal.image && new URL(animal.image).protocol !== 'blob:') return

    if (!animal.image) {
      await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAnimalApi}/${animalId}/image`, {
        method: 'delete'
      })
      return
    }

    const image = await fetch(animal.image)
    const imageFile = await image.blob()

    const body = new FormData()
    body.set('image', imageFile)

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAnimalApi}/${animalId}/image`, {
      method: 'post',
      body
    })
  }

  async function createTreatment(treatment: EditTreatment) {
    if (!animalDetails.value || treatment.animal !== animalDetails.value.id) {
      throw Error('Cannot create a treatment for an animal different than the one that is loaded')
    }

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudTreatmentApi}`, {
      method: 'post',
      body: JSON.stringify(treatment),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // INFO: This could be an improvement point, insert manually the returned
    // treatment instead of refetching the whole animal
    await fetchAnimal(animalDetails.value.id)
  }

  async function deleteTreatment(treatmentId: string) {
    if (
      !animalDetails.value ||
      !animalDetails.value.treatments.map((treatment) => treatment.id).includes(treatmentId)
    ) {
      throw Error(
        'Cannot delete a treatment that belongs to an animal different than the one that is loaded'
      )
    }

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudTreatmentApi}/${treatmentId}`, {
      method: 'delete'
    })

    animalDetails.value.treatments = animalDetails.value.treatments.filter(
      (treatment) => treatment.id !== treatmentId
    )
  }

  async function createAppointment(appointment: EditAppointment) {
    if (!animalDetails.value || appointment.animal !== animalDetails.value.id) {
      throw Error(
        'Cannot create an appointment for an animal different than the one that is loaded'
      )
    }

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAppointmentApi}`, {
      method: 'post',
      body: JSON.stringify(appointment),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // INFO: Improvement point, same as treatment
    await fetchAnimal(animalDetails.value.id)
  }

  async function deleteAppointment(appointmentId: string) {
    if (
      !animalDetails.value ||
      !animalDetails.value.appointments.map((appointment) => appointment.id).includes(appointmentId)
    ) {
      throw Error(
        'Cannot delete an appointment that belongs to an animal different than the one that is loaded'
      )
    }

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAppointmentApi}/${appointmentId}`, {
      method: 'delete'
    })

    animalDetails.value.appointments = animalDetails.value.appointments.filter(
      (appointment) => appointment.id !== appointmentId
    )
  }

  async function fetchReport() {
    const response = await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAnimalApi}/report`)

    if (!response.ok) throw Error(`Error backend response: ${await response.json()}`)

    const blob = await response.blob()

    const elem = window.document.createElement('a')
    elem.href = window.URL.createObjectURL(blob)
    elem.download = 'animal_report.pdf'

    document.body.appendChild(elem)
    elem.click()

    document.body.removeChild(elem)
  }

  return {
    animalList,
    animalDetails,
    isLoading,
    fetchAnimals,
    fetchAnimal,
    fetchReport,
    createAnimal,
    updateAnimal,
    createTreatment,
    deleteTreatment,
    createAppointment,
    deleteAppointment
  }
})
