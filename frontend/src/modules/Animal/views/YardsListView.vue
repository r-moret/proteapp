<script setup lang="ts">
import AppHeader from '@/skeleton/AppHeader.vue'
import YardList from '@/modules/Animal/components/YardList.vue'
import { onBeforeMount, ref } from 'vue'
import { useAnimalStore } from '@/store/AnimalStore'
import { storeToRefs } from 'pinia'
import TextInput from '@/components/TextInput.vue'
import ToastNotifications from '@/components/ToastNotifications.vue'
import type { EditYard } from '../declarations'
import { EditYardAdapter } from '@/modules/Animal/adapters'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { ZodError } from 'zod'
import BottomDrawer from '@/components/BottomDrawer.vue'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const animalStore = useAnimalStore()
const { yardList } = storeToRefs(animalStore)
const newYardForm = ref<HTMLFormElement | null>(null)
const newYard = ref<EditYard>()

async function handleAddYard(closeDrawer: () => void) {
  if (!newYard.value) return

  try {
    EditYardAdapter(newYard.value)

    await animalStore.createYard(newYard.value)
    showSuccessNotification('Adopción añadida correctamente.')

    newYardForm.value?.reset()
    newYard.value = {
      name: ''
    }

    closeDrawer()
  } catch (error) {
    if (error instanceof ZodError) {
      showErrorNotification('Parece que hay un error con los datos del patio.')
    } else {
      showErrorNotification('Ha ocurrido un error, prueba otra vez.')
    }
  }
}

onBeforeMount(async () => {
  await animalStore.fetchYards()
  newYard.value = {
    name: ''
  }
})

const newYardOpen = ref(false)
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificationsRef" />
    <AppHeader left="back" title="Patios">
      <button class="btn btn-square btn-ghost" @click="newYardOpen = true">
        <span class="i-mingcute-add-fill text-3xl" />
      </button>
    </AppHeader>
    <YardList :yard-list="yardList"></YardList>
    <BottomDrawer class="bg-base-200" size="small" v-model="newYardOpen" v-slot="{ close }">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Nuevo patio</h1>
        <form
          v-if="newYard"
          ref="newYardForm"
          class="flex h-full flex-col gap-6 pb-10"
          @submit.prevent="handleAddYard(close)"
        >
          <div class="flex flex-col gap-2">
            <label class="font-semibold" for="new-yard-name"> Nombre del patio </label>
            <TextInput name="new-yard-name" placeholder="ej. Patio 1" v-model="newYard.name" />
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
