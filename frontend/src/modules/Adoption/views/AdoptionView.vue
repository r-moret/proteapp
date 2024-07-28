<script setup lang="ts">
import { useParams } from '@/composable/useParams'
import { useAdoptionStore } from '@/store/AdoptionStore'
import AppHeader from '@/skeleton/AppHeader.vue'
import { computed, onBeforeMount, ref } from 'vue'
import { storeToRefs } from 'pinia'
import humanizeDuration from 'humanize-duration'
import { format, addDay } from '@formkit/tempo'
import BottomDrawer from '@/components/BottomDrawer.vue'
import ItemList from '@/components/ItemList.vue'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { EditMonitoringAdapter } from '@/modules/Adoption/adapters'
import type { EditMonitoring } from '../declarations'
import { ZodError } from 'zod'
import TextInput from '@/components/TextInput.vue'
import DateInput from '@/components/DateInput.vue'
const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)
const placeholderImage = computed(() => '/images/dog.png')
const routeParams = useParams<{ id: string }>()
const adoptionStore = useAdoptionStore()
const { adoptionDetails, isLoading } = storeToRefs(adoptionStore)

const fullname = computed(() => {
  const name = adoptionDetails.value?.person.name
  const firstSurname = adoptionDetails.value?.person.firstSurname
  const secondSurname = adoptionDetails.value?.person.secondSurname || ''
  return `${name} ${firstSurname}${secondSurname ? ' ' + secondSurname : ''}`
})

const age = computed(() => {
  if (!adoptionDetails.value || !adoptionDetails.value.animal.birthDate) return

  const ageMs = Math.max(
    1 * 24 * 60 * 60 * 1000, // 1 day is the smallest amount of time displayed
    new Date().valueOf() - adoptionDetails.value.animal.birthDate.valueOf()
  )
  return humanizeDuration(ageMs, {
    language: 'es',
    units: ['y', 'mo', 'd'],
    largest: 1,
    round: false
  })
})

const newMonitoringOpen = ref(false)
const newMonitoringForm = ref<HTMLFormElement | null>(null)
const newMonitoring = ref<EditMonitoring>()

const phone_number = computed(() => {
  if (!adoptionDetails.value || !adoptionDetails.value.person.phone) return
  return adoptionDetails.value.person.phone.substring(3)
})

async function handleDeleteMonitoring(monitoringId: string) {
  try {
    await adoptionStore.deleteMonitoring(monitoringId)
    showSuccessNotification(' eliminada correctamente')
  } catch (error) {
    showErrorNotification('Ha ocurrido un error, prueba otra vez.')
  }
}

async function handleAddMonitoring(closeDrawer: () => void) {
  if (!adoptionDetails.value || !newMonitoring.value) return

  try {
    newMonitoring.value.followDate = new Date(
      newMonitoring.value.followDate.getFullYear(),
      newMonitoring.value.followDate.getMonth(),
      newMonitoring.value.followDate.getDate()
    )
    console.log(newMonitoring.value)
    EditMonitoringAdapter(newMonitoring.value)

    await adoptionStore.createMonitoring(newMonitoring.value)
    showSuccessNotification('Seguimiento añadido correctamente.')

    newMonitoringForm.value?.reset()
    newMonitoring.value = {
      followDate: addDay(new Date()),
      note: '',
      adoption: adoptionDetails.value.id
    }
    closeDrawer()
  } catch (error) {
    if (error instanceof ZodError) {
      showErrorNotification('Parece que hay un error con los datos del seguimiento.')
    } else {
      showErrorNotification('Ha ocurrido un error, prueba otra vez.')
    }
  }
}

onBeforeMount(async () => {
  if (!adoptionDetails.value || adoptionDetails.value.id !== routeParams.value.id) {
    await adoptionStore.fetchAdoption(routeParams.value.id)
  }

  newMonitoring.value = {
    followDate: addDay(new Date()),
    note: '',
    adoption: adoptionDetails.value!.id
  }
})
</script>
<template>
  <main>
    <ToastNotifications ref="notificationsRef" />
    <AppHeader left="back" title="Adopción">
      <button class="btn btn-square btn-ghost" @click="newMonitoringOpen = true">
        <span class="i-mingcute-add-fill text-3xl" />
      </button>
    </AppHeader>
    <div class="px-5">
      <div v-if="isLoading" class="flex h-full w-full items-center justify-center">
        <span class="loading loading-spinner loading-lg text-secondary" />
      </div>
      <div v-else-if="adoptionDetails" class="grid min-h-0 flex-grow">
        <div class="flex w-full items-start gap-4">
          <div class="mx-3 my-4 flex flex-row gap-4">
            <img
              :class="['border-1 btn-square h-36 w-36 rounded-xl object-cover shadow-xl']"
              :src="adoptionDetails?.animal.image ?? placeholderImage"
              alt="Adoption animal avatar image"
            />
            <div>
              <span class="text-3xl font-semibold"
                >{{ adoptionDetails?.animal.name }},
                <span class="text-2xl font-normal italic"> {{ age }} </span>
              </span>
              <p class="my-3 font-semibold">{{ adoptionDetails?.animal.personality }}</p>
              <span class="my-2 flex items-center space-x-2">
                <span
                  :class="[
                    adoptionDetails?.animal.isCastrated
                      ? 'i-mingcute-lock-fill'
                      : 'i-mingcute-unlock-line',
                    'text-xl'
                  ]"
                >
                </span>
                <span class="font-medium">{{
                  adoptionDetails?.animal.isCastrated ? 'Castrado' : 'Sin castrar'
                }}</span>
              </span>
              <span class="flex items-center space-x-2">
                <div class="relative flex text-2xl">
                  <span
                    v-if="!adoptionDetails?.animal.isAnimalCompatible"
                    class="i-mingcute-line-fill absolute"
                  />
                  <span
                    :class="[
                      adoptionDetails?.animal.isAnimalCompatible
                        ? 'i-mingcute-paw-fill'
                        : 'i-mingcute-paw-line',
                      'text-2xl'
                    ]"
                  />
                </div>
                <span class="font-medium">{{
                  adoptionDetails?.animal.isAnimalCompatible ? 'Compatible' : 'No compatible'
                }}</span>
              </span>
            </div>
          </div>
        </div>
        <p class="mx-3 mb-2 text-2xl font-bold">Adoptante</p>
        <article
          :class="[
            'mb-5 flex items-center gap-4 rounded-2xl bg-secondary-content px-3 py-2 shadow-sm'
          ]"
        >
          <section class="px-2 py-1">
            <header class="flex items-center">
              <p class="text-lg font-semibold">{{ fullname }}</p>
            </header>
            <span class="italic"> {{ adoptionDetails?.person.email }} </span>
            <span> - </span>
            <span class="italic">{{ phone_number }}</span>
          </section>
        </article>
        <p class="mx-3 mb-2 text-2xl font-bold">Seguimientos</p>
        <ItemList
          :items="adoptionDetails?.monitorings"
          delete-title="¿Estás seguro de que quieres borrar este seguimiento?"
          @delete="(monitoring) => handleDeleteMonitoring(monitoring.id)"
          class="mx-5 mt-4"
        >
          <template #empty>
            <div class="mt-6 flex flex-col items-center">
              <span class="i-mingcute-diary-fill text-6xl" />
              <p class="text-gray-500">{{ adoptionDetails?.animal.name }} no tiene seguimientos</p>
            </div>
          </template>
          <template #item="{ item, openConfirm }">
            <div class="flex flex-row justify-between py-2">
              <div class="flex flex-col">
                <p class="mb-1 text-lg font-semibold text-secondary">
                  {{ format(item.followDate, { date: 'long' }) }}
                </p>
                <p class="text-base text-gray-700">
                  {{ item.note }}
                </p>
              </div>
              <button class="my-1 flex flex-col" @click="openConfirm(item)">
                <span class="i-mingcute-close-fill text-xl text-gray-400" />
              </button>
            </div>
          </template>
          <template #delete="{ item }">
            <p>
              <span class="font-semibold">{{ format(item.followDate, { date: 'long' }) }}</span>
            </p>
          </template>
        </ItemList>
      </div>
    </div>
    <BottomDrawer class="bg-base-200" size="small" v-model="newMonitoringOpen" v-slot="{ close }">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Nuevo seguimiento</h1>
        <form
          v-if="newMonitoring"
          ref="newMonitoringForm"
          class="flex h-full flex-col gap-6 pb-10"
          @submit.prevent="handleAddMonitoring(close)"
        >
          <div class="flex flex-col gap-2">
            <label class="font-semibold" for="new-monitoring-description">
              Descripción del seguimiento
            </label>
            <TextInput
              name="new-monitoring-description"
              placeholder="ej. Adaptado correctamente"
              v-model="newMonitoring.note"
            />
          </div>

          <div class="flex flex-col gap-2">
            <label class="font-semibold" for="">Fecha seguimiento</label>
            <DateInput
              :include-time="false"
              placeholder="ej. 23 de mayo de 2023"
              v-model="newMonitoring.followDate"
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
