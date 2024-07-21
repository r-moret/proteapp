<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import { useAnimalStore } from '@/store/AnimalStore'
import { useParams } from '@/composable/useParams'
import { storeToRefs } from 'pinia'
import ItemList from '@/components/ItemList.vue'
import { sortBy, reverse } from 'lodash'
import { format, addDay } from '@formkit/tempo'
import BottomDrawer from '@/components/BottomDrawer.vue'
import TextInput from '@/components/TextInput.vue'
import DateInput from '@/components/DateInput.vue'
import { EditAppointmentAdapter } from '@/modules/Animal/adapters'
import { ZodError } from 'zod'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { useToastNotifications } from '@/composable/useToastNotifications'
import type { EditAppointment } from '../declarations'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const animalStore = useAnimalStore()
const { animalDetails, isLoading } = storeToRefs(animalStore)

const routeParams = useParams<{ id: string }>()

const newAppointmentOpen = ref(false)
const newAppointmentForm = ref<HTMLFormElement | null>(null)
const newAppointment = ref<EditAppointment>()

const sortedAppointments = computed(() =>
  reverse(sortBy(animalDetails.value?.appointments, ['date']))
)

async function handleAddAppointment(closeDrawer: () => void) {
  if (!animalDetails.value || !newAppointment.value) return

  try {
    EditAppointmentAdapter(newAppointment.value)

    await animalStore.createAppointment(newAppointment.value)
    showSuccessNotification('Cita médica añadida correctamente.')

    newAppointmentForm.value?.reset()
    newAppointment.value = {
      date: addDay(new Date()),
      description: '',
      animal: animalDetails.value.id
    }
    closeDrawer()
  } catch (error) {
    if (error instanceof ZodError) {
      showErrorNotification('Parece que hay un error con los datos de la cita.')
    } else {
      showErrorNotification('Ha ocurrido un error, prueba otra vez.')
    }
  }
}

async function handleDeleteAppointment(appointmentId: string) {
  try {
    await animalStore.deleteAppointment(appointmentId)
    showSuccessNotification('Cita médica eliminada correctamente')
  } catch (error) {
    showErrorNotification('Ha ocurrido un error, prueba otra vez.')
  }
}

onBeforeMount(async () => {
  if (!animalDetails.value || animalDetails.value.id !== routeParams.value.id) {
    await animalStore.fetchAnimal(routeParams.value.id)
  }

  newAppointment.value = {
    date: addDay(new Date()),
    description: '',
    animal: animalDetails.value!.id
  }
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificationsRef" />

    <AppHeader left="back" title="Citas médicas" />

    <div v-if="isLoading" class="flex h-full w-full items-center justify-center">
      <span class="loading loading-spinner loading-lg text-secondary" />
    </div>

    <div v-else-if="animalDetails" class="grid min-h-0 flex-grow">
      <div class="col-start-1 row-start-1 min-h-0">
        <div class="flex h-full w-full flex-col">
          <ItemList
            :items="sortedAppointments"
            delete-title="¿Estás seguro de que quieres borrar esta cita médica?"
            class="mx-5"
            @delete="(appointment) => handleDeleteAppointment(appointment.id)"
          >
            <template #empty>
              <div class="mt-6 flex flex-col items-center">
                <span class="i-mingcute-calendar-time-add-line text-6xl" />
                <p class="text-gray-500">{{ animalDetails.name }} no tiene citas médicas</p>
              </div>
            </template>

            <template #item="{ item, openConfirm }">
              <div class="flex flex-row justify-between px-4 py-2">
                <div class="flex flex-col">
                  <p
                    :class="[
                      'mb-1 text-lg font-semibold',
                      item.isPast ? 'text-gray-400' : 'text-secondary'
                    ]"
                  >
                    {{ item.description }}
                  </p>
                  <p :class="['text-base', item.isPast ? 'text-gray-400' : 'text-gray-700']">
                    {{ format(item.date, { date: 'long', time: 'short' }) }}
                  </p>
                </div>
                <button v-if="!item.isPast" class="my-1 flex flex-col" @click="openConfirm(item)">
                  <span class="i-mingcute-close-fill text-xl text-gray-400" />
                </button>
              </div>
            </template>

            <template #delete="{ item }">
              <p>
                <span class="font-semibold">{{ item.description }}</span>
                <span>
                  {{
                    `, el día ${format(item.date, { date: 'long' })} a las ${format(item.date, { time: 'short' })}`
                  }}
                </span>
              </p>
            </template>
          </ItemList>
        </div>
      </div>

      <div class="z-10 col-start-1 row-start-1 justify-end place-self-end p-4">
        <button
          @click="newAppointmentOpen = true"
          class="z-10 flex items-center justify-center rounded-full bg-blue-500 p-4 text-white shadow-lg"
        >
          <span class="i-mingcute-add-fill text-xl" />
        </button>
      </div>
    </div>

    <BottomDrawer class="bg-base-200" size="small" v-model="newAppointmentOpen" v-slot="{ close }">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Nueva cita médica</h1>
        <form
          v-if="newAppointment"
          ref="newAppointmentForm"
          class="flex h-full flex-col gap-6 pb-10"
          @submit.prevent="handleAddAppointment(close)"
        >
          <div class="flex flex-col gap-2">
            <label class="font-semibold" for="new-appointment-description">
              Descripción de la cita
            </label>
            <TextInput
              name="new-appointment-description"
              placeholder="ej. Vacuna calcivirus"
              v-model="newAppointment.description"
            />
          </div>

          <div class="flex flex-col gap-2">
            <label class="font-semibold" for="">Fecha de la cita</label>
            <DateInput
              :include-time="true"
              placeholder="ej. 23 de mayo de 2023, 18:30"
              v-model="newAppointment.date"
            />
          </div>

          <button
            class="mt-auto w-fit self-center rounded-lg bg-secondary px-10 py-3 text-xl font-semibold text-white"
          >
            Añadir
          </button>
        </form>
      </div>
    </BottomDrawer>
  </main>
</template>
