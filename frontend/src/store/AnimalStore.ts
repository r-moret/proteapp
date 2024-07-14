import { ref } from 'vue'
import { defineStore } from 'pinia'
import type {
  Animal,
  Appointment,
  CreateAppointment,
  Treatment,
  Yard
} from '@/modules/Animal/declarations'
import {
  listAnimal as listAnimalApi,
  listYards as listYardApi,
  crudAnimal as crudAnimalApi,
  crudTreatment as crudTreatmentApi,
  crudAppointment as crudAppointmentApi
} from '@/modules/Animal/api'
import { AnimalAdapter, AppointmentAdapter, TreatmentAdapter } from '@/modules/Animal/adapters'

export const useAnimalStore = defineStore('AnimalStore', () => {
  const animalList = ref<Animal[]>([])
  const animalDetails = ref<Animal>()

  const yardList = ref<Yard[]>([])

  const isLoading = ref(false)
  const isSaving = ref(false)

  async function fetchAnimals() {
    isLoading.value = true

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${listAnimalApi}`)
      .then((res) => res.json())
      .then((json) => json.map(AnimalAdapter))
      .then((animals) => (animalList.value = animals))

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${listYardApi}`)
      .then((res) => res.json())
      .then((json: Yard[]) => (yardList.value = json))

    isLoading.value = false
  }

  async function getAnimal(id: number) {
    isLoading.value = true

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAnimalApi}/${id}`)
      .then((res) => res.json())
      .then(AnimalAdapter)
      .then((animal) => (animalDetails.value = animal))

    isLoading.value = false
  }

  async function createTreatment(treatment: Treatment) {
    if (!animalDetails.value || treatment.animalId !== animalDetails.value?.id) {
      throw Error('Cannot create a treatment for an animal different than the one that is loaded')
    }

    // TODO: Add treatment validation

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudTreatmentApi}`, {
      method: 'post',
      body: JSON.stringify(treatment),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then((res) => res.json())
      .then(TreatmentAdapter)
      .then((treatment) => {
        if (!animalDetails.value || treatment.animalId !== animalDetails.value?.id) {
          throw Error(
            'Cannot create a treatment for an animal different than the one that is loaded'
          )
        }

        animalDetails.value.treatments = [...(animalDetails.value.treatments ?? []), treatment]
      })
  }

  async function deleteTreatment(treatment: Treatment) {
    if (!animalDetails.value || treatment.animalId !== animalDetails.value?.id) {
      throw Error('Cannot create a treatment for an animal different than the one that is loaded')
    }

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudTreatmentApi}/${treatment.id}`, {
      method: 'delete'
    })

    animalDetails.value.treatments = animalDetails.value.treatments?.filter(
      (treat) => treat.id !== treatment.id
    )
  }

  async function createAppointment(appointment: CreateAppointment) {
    if (!animalDetails.value || appointment.animalId !== animalDetails.value?.id) {
      throw Error(
        'Cannot create an appointment for an animal different than the one that is loaded'
      )
    }

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAppointmentApi}`, {
      method: 'post',
      body: JSON.stringify(appointment),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then((res) => res.json())
      .then(AppointmentAdapter)
      .then((appointment) => {
        if (!animalDetails.value || appointment.animalId !== animalDetails.value?.id) {
          throw Error(
            'Cannot create an appointment for an animal different than the one that is loaded'
          )
        }

        animalDetails.value.appointments = [
          ...(animalDetails.value.appointments ?? []),
          appointment
        ]
      })
  }

  async function deleteAppointment(appointment: Appointment) {
    if (!animalDetails.value || appointment.animalId !== animalDetails.value?.id) {
      throw Error(
        'Cannot delete an appointment for an animal different than the one that is loaded'
      )
    }

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudAppointmentApi}/${appointment.id}`, {
      method: 'delete'
    })

    animalDetails.value.appointments = animalDetails.value.appointments?.filter(
      (appo) => appo.id !== appointment.id
    )
  }

  return {
    animalList,
    animalDetails,
    yardList,
    isLoading,
    fetchAnimals,
    getAnimal,
    createTreatment,
    deleteTreatment,
    createAppointment,
    deleteAppointment
  }
})
