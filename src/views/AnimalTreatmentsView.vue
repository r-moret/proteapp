<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTreatmentStore } from '@/store/TreatmentStore'
import { useAnimalStore } from '@/store/AnimalStore'
import { storeToRefs } from 'pinia'

const { getAnimal } = useAnimalStore()
const { treatmentList } = storeToRefs(useTreatmentStore())

const route = useRoute()

const animal = computed(() => {
  const foundAnimal = getAnimal(route.params.id as string)
  if (!foundAnimal) {
    throw Error('Animal not found')
  }
  return foundAnimal
})

const modalOpen = ref(false)

const newTreatment = ref({
  name: '',
  zone: '',
  freq: 0
})

const openModal = () => {
  modalOpen.value = true
}

const closeModal = () => {
  modalOpen.value = false
}

const saveTratamiento = () => {
  treatmentList.value.push({
    id: crypto.randomUUID(),
    animalId: animal.value.id,
    name: newTreatment.value.name,
    zone: newTreatment.value.zone,
    freq: newTreatment.value.freq
  })
  closeModal()
  // Limpiar el formulario después de guardar
  newTreatment.value = { name: '', zone: '', freq: 0 }
}

const removeTratamiento = (index: number) => {
  treatmentList.value.splice(index, 1)
}
</script>

<template>
  <main class="flex flex-col">
    <AppHeader left="profile" title="Citas médicas" />
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
            <p class="text-2xl">2 de septiembre 15:00</p>
          </div>
        </div>
        <p class="text-center text-lg text-gray-600">Motivo: vacuna</p>
      </div>
    </div>

    <div class="mt-5 flex h-3/4 w-full flex-col pb-16">
      <div class="mt-4 flex items-center justify-center">
        <p class="text-2xl font-bold text-gray-700">Tratamientos</p>
      </div>
      <div class="mx-5 mt-4 flex-1 overflow-y-auto">
        <ul class="space-y-2">
          <li
            v-for="(treatment, index) in treatmentList"
            :key="index"
            class="relative flex flex-col rounded-lg p-4 shadow-sm transition hover:bg-gray-200"
          >
            <span
              class="i-mingcute-close-fill absolute right-2 top-4 h-6 w-6 cursor-pointer text-gray-500"
              @click="removeTratamiento(index)"
            ></span>
            <p class="text-lg font-semibold text-blue-600">{{ treatment.name }}</p>
            <p class="text-base text-gray-700">Zona: {{ treatment.zone }}</p>
            <p class="text-base text-gray-700">Frecuencia: {{ treatment.freq }}</p>
          </li>
        </ul>
      </div>
    </div>

    <!-- Botón flotante para abrir el modal -->
    <button
      @click="openModal"
      class="fixed bottom-10 right-10 rounded-full bg-blue-500 px-8 py-4 text-white shadow-lg"
    >
      Añadir tratamiento
    </button>

    <!-- Modal para añadir tratamiento -->
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
          <form @submit.prevent="saveTratamiento">
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
  </main>
</template>
