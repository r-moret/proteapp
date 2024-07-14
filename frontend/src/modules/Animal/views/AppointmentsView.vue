<script setup lang="ts">
import { computed, ref } from 'vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import { useAnimalStore } from '@/store/AnimalStore'
import { useRoute } from 'vue-router'

const { getAnimal } = useAnimalStore()
const route = useRoute()
const animal = computed(() => getAnimal(Number(route.params.id as string)))

const modalOpen = ref(false)
const newAppointment = ref({
  date: new Date(2024, 5, 17, 18, 30),
  description: '',
  is_past: false
})

const openModal = () => {
  modalOpen.value = true
}

const closeModal = () => {
  modalOpen.value = false
}

const formatDate = (date: Date) => {
  const options: Intl.DateTimeFormatOptions = {
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return date.toLocaleDateString('es-ES', options)
}
</script>

<template>
  <main class="flex flex-col">
    <AppHeader left="back" title="Citas médicas" />
    <div class="grid min-h-0 flex-grow">
      <div class="col-start-1 row-start-1 min-h-0">
        <div class="flex h-full w-full flex-col">
          <!-- <div class="mt-4 flex items-center justify-center">
            <p class="text-2xl font-bold text-gray-700">Historial de citas</p>
          </div> -->
          <div class="mx-5 mt-4 flex-1 overflow-y-auto">
            <p v-if="!animal?.appointments?.length" class="mt-5 text-center">
              No hay citas médicas
            </p>
            <ul v-else class="space-y-2">
              <li
                v-for="(appointment, index) in animal.appointments"
                :key="index"
                class="relative flex flex-col rounded-lg p-4 shadow-sm transition hover:bg-gray-200"
              >
                <span
                  v-if="!appointment.is_past"
                  class="i-mingcute-close-fill absolute right-2 top-4 h-6 w-6 cursor-pointer text-gray-500"
                ></span>
                <p
                  :class="[
                    'mb-2 text-xl font-semibold',
                    appointment.is_past ? 'text-gray-400' : 'text-blue-600'
                  ]"
                >
                  {{ appointment.description }}
                </p>
                <div
                  :class="['flex items-center space-x-2', { 'text-gray-400': appointment.is_past }]"
                >
                  <span class="i-mingcute-calendar-time-add-line text-3xl" />
                  <p class="text-base">
                    {{ formatDate(appointment.date) }}
                  </p>
                </div>
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
                <!-- @submit.prevent="saveAppointment" -->
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">Motivo de la cita</span>
                  </label>
                  <input
                    v-model="newAppointment.description"
                    type="text"
                    class="input input-bordered"
                    required
                  />
                </div>
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">Fecha y hora</span>
                  </label>
                  <input
                    v-model="newAppointment.date"
                    type="datetime-local"
                    class="input input-bordered"
                    required
                  />
                </div>
                <div class="mt-4">
                  <button type="submit" class="btn w-full">Guardar cita médica</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
