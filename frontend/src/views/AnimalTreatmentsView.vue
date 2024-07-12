<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { format } from '@formkit/tempo'
import AppHeader from '@/skeleton/AppHeader.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import TextInput from '@/components/TextInput.vue'
import TimeInput from '@/components/TimeInput.vue'
import DateInput from '@/components/DateInput.vue'
import type { Animal, Treatment } from '@/modules/Animal/declarations'
import humanizeDuration from 'humanize-duration'

const router = useRouter()

const props = defineProps<{
  animal: Animal
}>()

const nextAppointment = computed(() => {
  if (!props.animal || !props.animal.appointments) return

  const futureAppointments = props.animal.appointments.filter((appointment) => !appointment.is_past)
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

const navigateAppointments = () => {
  // TODO: Using route props
  // router.push({ name: 'animal.appointments', params: { id: route.params.id } })
}

const newTreatmentForm = ref<HTMLFormElement | null>(null)
const newTreatment = ref<Treatment>({ name: '' })

function handleAddTreatment(closeDrawer: () => void) {
  // TODO
  newTreatmentForm.value?.reset()
  closeDrawer()
}
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
                v-for="(treatment, index) in props.animal.treatments"
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
