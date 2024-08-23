import { ref } from 'vue'
import { defineStore } from 'pinia'
import type {
  Animal,
  AnimalInfo,
  EditAppointment,
  EditTreatment
} from '@/modules/Animal/declarations'
import {
  listAnimal as listAnimalApi,
  crudAnimal as crudAnimalApi,
  crudTreatment as crudTreatmentApi,
  crudAppointment as crudAppointmentApi
} from '@/modules/Animal/api'

import { listYards as listYardApi } from '@/modules/Yard/api'
import type { Yard } from '@/modules/Yard/declarations'
import { AnimalAdapter, AnimalInfoAdapter } from '@/modules/Animal/adapters'
import { authFetch } from '@/composable/useAuthFetch'

export const useAnimalStore = defineStore('AnimalStore', () => {
  const animalList = ref<AnimalInfo[]>([])
  const animalDetails = ref<Animal>()
  const yardList = ref<Yard[]>([])
  const isLoading = ref(false)

  async function fetchAnimals() {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${listAnimalApi}`)
      .then((res) => res.json())
      .then((json) => json.map(AnimalInfoAdapter))
      .then((animals) => (animalList.value = animals))

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${listYardApi}`)
      .then((res) => res.json())
      .then((json: Yard[]) => (yardList.value = json))

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

  return {
    animalList,
    animalDetails,
    isLoading,
    fetchAnimals,
    fetchAnimal,
    createTreatment,
    deleteTreatment,
    createAppointment,
    deleteAppointment
  }
})
