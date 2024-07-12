<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { format } from '@formkit/tempo'
import AppHeader from '@/skeleton/AppHeader.vue'
import { useAnimalStore } from '@/store/AnimalStore'
import humanizeDuration from 'humanize-duration'

const { getAnimal } = useAnimalStore()
const router = useRouter()
const route = useRoute()

const animal = computed(() => getAnimal(Number(route.params.id as string)))
const treatments = animal.value?.treatments

const nextAppointment = computed(() => {
  if (!animal.value || !animal.value.appointments) return
  const futureAppointments = animal.value.appointments.filter((appointment) => !appointment.is_past)
  if (futureAppointments.length === 0) return

  return futureAppointments.reduce((closest, appointment) =>
    !closest || appointment.date < closest.date ? appointment : closest
  )
})

function formatFrequency(minutes: number): string {
  if (minutes === 1440) {
    return 'una vez al día'
  }

  const milliseconds = minutes * 60 * 1000
  return `cada ${humanizeDuration(milliseconds, { language: 'es', units: ['w', 'd', 'h', 'm'], round: true, conjunction: ' y ' })}`
}

const navigateAppointments = () =>
  router.push({ name: 'animal.appointments', params: { id: route.params.id } })

const modalOpen = ref(false)
const newTreatment = ref({
  name: '',
  zone: '',
  freq: ''
})

const openModal = () => {
  modalOpen.value = true
}

const closeModal = () => {
  modalOpen.value = false
}

// const saveTratamiento = () => {
//   treatments?.value.push({
//     name: newTreatment.value.name,
//     zone: newTreatment.value.zone,
//     freq: newTreatment.value.freq
//   })
//   closeModal()
//   // Limpiar el formulario después de guardar
//   newTreatment.value = { name: '', zone: '', freq: '' }
// }

// const removeTratamiento = (index: number) => {
//   treatments.value.splice(index, 1)
// }
</script>

<template>
  <main class="flex flex-col">
    <AppHeader left="back" title="Tratamientos">
      <button class="btn btn-square btn-ghost" @click="navigateAppointments">
        <span class="i-mingcute-hospital-line text-3xl" />
      </button>
    </AppHeader>

    <div class="grid min-h-0 flex-grow">
      <div class="col-start-1 row-start-1 min-h-0">
        <div class="flex h-1/4 w-full flex-col items-center justify-center">
          <div class="w-full max-w-md rounded-lg p-4">
            <div class="mb-5 flex items-center justify-center">
              <p class="text-2xl font-bold text-gray-700">Próxima cita médica</p>
            </div>
            <div class="flex items-center justify-center">
              <div
                class="mb-5 flex items-center justify-center gap-4 rounded-2xl bg-blue-500 px-6 py-4 text-white shadow-lg"
              >
                <span class="i-mingcute-calendar-2-fill text-5xl"></span>
                <p v-if="nextAppointment?.date" class="text-2xl">
                  {{ format(nextAppointment?.date, 'long', 'es-ES') }}
                </p>
                <p v-else class="text-xl">No hay cita médica</p>
              </div>
            </div>
            <p v-if="nextAppointment?.date" class="text-center text-lg text-gray-600">
              {{ nextAppointment.description }}
            </p>
          </div>
        </div>

        <div class="flex h-3/4 w-full flex-col">
          <div class="mt-4 flex items-center justify-center">
            <p class="text-2xl font-bold text-gray-700">Tratamientos</p>
          </div>
          <div class="mx-5 mt-4 flex-1 overflow-y-auto">
            <p v-if="!animal?.treatments?.length" class="mt-5 text-center">No hay tratamientos</p>
            <ul v-else class="space-y-2">
              <li
                v-for="(treatment, index) in treatments"
                :key="index"
                class="relative flex flex-col rounded-lg p-4 shadow-sm transition hover:bg-gray-200"
              >
                <span
                  class="i-mingcute-close-fill absolute right-2 top-4 h-6 w-6 cursor-pointer text-gray-500"
                ></span>
                <p class="text-lg font-semibold text-blue-600">{{ treatment.name }}</p>
                <p v-if="treatment.zone" class="text-base text-gray-700">
                  Zona: {{ treatment.zone }}
                </p>
                <p v-if="treatment.frequency" class="text-base text-gray-700">
                  Frecuencia: {{ formatFrequency(treatment.frequency) }}
                </p>
                <p v-if="treatment.amount" class="text-base text-gray-700">
                  Cantidad: {{ treatment.amount }}
                </p>
                <p v-if="treatment.final_date" class="text-base text-gray-700">
                  Fecha de finalización: {{ format(treatment.final_date, 'medium', 'es-ES') }}
                </p>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col-start-1 row-start-1 flex flex-col items-end justify-end p-4">
        <button
          @click="openModal"
          class="z-10 flex items-center justify-center rounded-full bg-blue-500 p-4 text-white shadow-lg"
        >
          <span class="i-mingcute-add-fill text-xl" />
        </button>

        <div
          :class="{ hidden: !modalOpen }"
          class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto"
        >
          <div class="relative mx-auto w-full max-w-sm rounded-lg bg-white p-8 shadow-lg">
            <button
              @click="closeModal"
              class="absolute right-4 top-4 text-gray-500 hover:text-gray-700"
            >
              <span class="i-mingcute-close-fill h-6 w-6"></span>
            </button>
            <div class="mb-4">
              <h2 class="mb-4 text-2xl font-semibold text-gray-800">Añadir tratamiento</h2>
              <form>
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">Nombre</span>
                  </label>
                  <input
                    v-model="newTreatment.name"
                    type="text"
                    class="input input-bordered"
                    required
                  />
                </div>
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">Zona</span>
                  </label>
                  <input
                    v-model="newTreatment.zone"
                    type="text"
                    class="input input-bordered"
                    required
                  />
                </div>
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">Frecuencia</span>
                  </label>
                  <input
                    v-model="newTreatment.freq"
                    type="text"
                    class="input input-bordered"
                    required
                  />
                </div>
                <div class="mt-4">
                  <button type="submit" class="btn w-full">Guardar tratamiento</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
