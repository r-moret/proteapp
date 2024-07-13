<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { format } from '@formkit/tempo'
import AppHeader from '@/skeleton/AppHeader.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import TextInput from '@/components/TextInput.vue'
import TimeInput from '@/components/TimeInput.vue'
import DateInput from '@/components/DateInput.vue'
import ToastNotifications from '../components/ToastNotifications.vue'
import type { Treatment } from '@/modules/Animal/declarations'
import humanizeDuration from 'humanize-duration'
import { useAnimalStore } from '@/store/AnimalStore'
import { storeToRefs } from 'pinia'
import { useToastNotifications } from '@/composable/useToastNotifications'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const animalStore = useAnimalStore()
const { animalDetails, isLoading } = storeToRefs(animalStore)

const router = useRouter()
const route = useRoute()

const { id }: { id?: string } = route.params

const nextAppointment = computed(() => {
  if (!animalDetails.value || !animalDetails.value.appointments) return

  const futureAppointments = animalDetails.value.appointments.filter(
    (appointment) => !appointment.isPast
  )
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

function navigateAppointments() {
  router.push({ name: 'animal.appointments', params: { id } })
}

const newTreatmentForm = ref<HTMLFormElement | null>(null)
const newTreatment = ref<Treatment>({ name: '', animalId: animalDetails.value?.id })

async function handleAddTreatment(closeDrawer: () => void) {
  if (!animalDetails.value || !newTreatment.value) return

  // TODO: Add treatment validation
  try {
    await animalStore.createTreatment(newTreatment.value)
    showSuccessNotification('Tratamiento añadido correctamente.')

    newTreatmentForm.value?.reset()
    closeDrawer()
  } catch (error) {
    showErrorNotification('Ha ocurrido un error, prueba otra vez.')
  }
}

onBeforeMount(async () => {
  if (!animalDetails.value || animalDetails.value.id !== Number(id)) {
    await animalStore.getAnimal(Number(id))
    newTreatment.value.animalId = animalDetails.value?.id
  }
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificationsRef" />

    <AppHeader left="back" title="Tratamientos">
      <button class="btn btn-square btn-ghost" @click="navigateAppointments">
        <span class="i-mingcute-hospital-line text-3xl" />
      </button>
    </AppHeader>

    <div v-if="isLoading" class="flex h-full w-full items-center justify-center">
      <span class="loading loading-spinner loading-lg text-secondary" />
    </div>

    <div v-else-if="animalDetails" class="grid min-h-0 flex-grow">
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
            <p v-if="!animalDetails.treatments?.length" class="mt-5 text-center">
              No hay tratamientos
            </p>
            <ul v-else class="space-y-2">
              <li
                v-for="(treatment, index) in animalDetails.treatments"
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
                <p v-if="treatment.endDate" class="text-base text-gray-700">
                  Fecha de finalización: {{ format(treatment.endDate, 'medium', 'es-ES') }}
                </p>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div class="z-10 col-start-1 row-start-1 place-self-end justify-self-end p-4">
        <BottomDrawer class="bg-base-200" size="big">
          <template #button="{ open }">
            <button
              @click="open"
              class="flex items-center justify-center rounded-full bg-secondary p-4 text-white"
            >
              <span class="i-mingcute-add-fill text-xl" />
            </button>
          </template>

          <template #drawer="{ close }">
            <div class="flex h-full flex-col gap-5">
              <h1 class="text-3xl font-semibold">Nuevo tratamiento</h1>
              <form
                @submit.prevent="handleAddTreatment(close)"
                ref="newTreatmentForm"
                class="flex h-full flex-col gap-6 pb-10"
              >
                <div class="flex flex-col gap-2">
                  <label class="font-semibold" for="new-treatment-name">
                    Nombre del tratamiento
                  </label>
                  <TextInput
                    name="new-treatment-name"
                    placeholder="ej. Clorexhidina"
                    v-model="newTreatment.name"
                  />
                </div>

                <div class="flex flex-col gap-2">
                  <label class="font-semibold" for="new-treatment-zone">Zona de aplicación</label>
                  <TextInput
                    name="new-treatment-zone"
                    placeholder="ej. Pata superior derecha"
                    v-model="newTreatment.zone"
                  />
                </div>

                <div class="flex flex-col gap-2">
                  <label class="font-semibold" for="new-treatment-freq">Aplicar cada</label>
                  <TimeInput
                    name="new-treatment-freq"
                    time-size="small"
                    :units="['d', 'h', 'min']"
                    v-model="newTreatment.frequency"
                  />
                </div>

                <div class="flex flex-col gap-2">
                  <label class="font-semibold" for="new-treatment-quantity">
                    Cantidad a aplicar
                  </label>
                  <TextInput
                    name="new-treatment-quantity"
                    placeholder="ej. Media pastilla"
                    v-model="newTreatment.amount"
                  />
                </div>

                <div class="flex flex-col gap-2">
                  <label class="font-semibold" for="">Fecha de finalización</label>
                  <DateInput
                    :include-time="false"
                    placeholder="ej. 23 de mayo de 2023"
                    v-model="newTreatment.endDate"
                  />
                </div>

                <button
                  class="mt-auto w-fit self-center rounded-lg bg-secondary px-10 py-3 text-xl font-semibold text-white"
                >
                  Añadir
                </button>
              </form>
            </div>
          </template>
        </BottomDrawer>
      </div>
    </div>
  </main>
</template>
