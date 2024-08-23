<script setup lang="ts">
import AppHeader from '@/skeleton/AppHeader.vue'
import YardList from '@/modules/Yard/components/YardList.vue'
import { onBeforeMount, ref } from 'vue'
import { useYardStore } from '@/store/YardStore'
import { storeToRefs } from 'pinia'
import TextInput from '@/components/TextInput.vue'
import ToastNotifications from '@/components/ToastNotifications.vue'
import type { EditYard } from '../declarations'
import { EditYardAdapter } from '@/modules/Yard/adapters'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { ZodError } from 'zod'
import BottomDrawer from '@/components/BottomDrawer.vue'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const yardStore = useYardStore()
const { lastYardOrder } = storeToRefs(yardStore)

const newYardForm = ref<HTMLFormElement | null>(null)
const newYard = ref<EditYard>()

async function addYardOrder() {
  if (!lastYardOrder.value) {
    return
  }
  const newYardOrder = {
    date: new Date(),
    yardOrder: lastYardOrder.value.map((item) => item.id)
  }
  yardStore.postYardOrder(newYardOrder)
  showSuccessNotification('Nuevo orden de patio guardado.')
  await yardStore.fetchLastYardOrder()
}

async function handleAddYard(closeDrawer: () => void) {
  if (!newYard.value) return

  try {
    EditYardAdapter(newYard.value)

    await yardStore.createYard(newYard.value)
    await yardStore.fetchYards()
    await yardStore.fetchLastYardOrder()
    showSuccessNotification('Patio añadido correctamente.')

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
  await yardStore.fetchLastYardOrder()
  await yardStore.fetchYards()

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
      <button class="btn btn-square btn-ghost" @click="addYardOrder">
        <span class="i-mingcute-save-2-line text-3xl" />
      </button>
      <button class="btn btn-square btn-ghost" @click="newYardOpen = true">
        <span class="i-mingcute-add-fill text-3xl" />
      </button>
    </AppHeader>

    <YardList v-if="lastYardOrder" :yard-list="lastYardOrder"></YardList>

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
