<script setup lang="ts">
import AppHeader from '@/skeleton/AppHeader.vue'
import YardList from '@/modules/Yard/components/YardList.vue'
import TextInput from '@/components/TextInput.vue'
import ToastNotifications from '@/components/ToastNotifications.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'

import { onBeforeMount, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { ZodError } from 'zod'

import { EditYardAdapter } from '@/modules/Yard/adapters'
import { useAuthStore } from '@/store/AuthStore'
import { useYardStore } from '@/store/YardStore'
import { useToastNotifications } from '@/composable/useToastNotifications'

import type { EditYard, YardInfo } from '@/modules/Yard/declarations'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const yardStore = useYardStore()
const { currentOrder } = storeToRefs(yardStore)

const authStore = useAuthStore()
const { isAdmin } = storeToRefs(authStore)

const newYardForm = ref<HTMLFormElement | null>(null)
const newYard = ref<EditYard>()
const editingYardOrder = ref(currentOrder.value)
const isNewYardOpen = ref(false)
const isEditOrderMode = ref(false)

function handleCancelEditOrder() {
  if (!currentOrder.value) return

  isEditOrderMode.value = false
  editingYardOrder.value = { ...currentOrder.value }
}

async function handleSaveYardOrder() {
  if (!editingYardOrder.value) return

  const newYardOrder = {
    date: new Date(),
    yardOrder: editingYardOrder.value.yardOrder.map((item) => item.id)
  }

  try {
    await yardStore.createOrder(newYardOrder)
    showSuccessNotification('Nuevo orden de patio guardado.')
  } catch (error) {
    showErrorNotification('Un error inesperado ocurrió mientras se guardaba el nuevo orden.')
    return
  }

  await yardStore.fetchCurrentOrder()
  editingYardOrder.value = { ...currentOrder.value! }

  isEditOrderMode.value = false
}

async function handleDeleteYard(yard: YardInfo) {
  try {
    await yardStore.deleteYard(yard.id)

    await yardStore.fetchCurrentOrder()
    editingYardOrder.value = { ...currentOrder.value! }

    showSuccessNotification('Patio eliminado correctamente')
  } catch (error) {
    showErrorNotification('Ha ocurrido un error, prueba otra vez.')
  }
}

async function handleAddYard(closeDrawer: () => void) {
  if (!newYard.value) return

  try {
    EditYardAdapter(newYard.value)

    await yardStore.createYard(newYard.value)
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

  await yardStore.fetchYards()

  await yardStore.fetchCurrentOrder()
  editingYardOrder.value = { ...currentOrder.value! }
}

onBeforeMount(async () => {
  await yardStore.fetchYards()

  await yardStore.fetchCurrentOrder()
  editingYardOrder.value = { ...currentOrder.value! }

  newYard.value = {
    name: ''
  }
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificationsRef" />
    <AppHeader left="back" title="Patios">
      <template v-if="isEditOrderMode">
        <button class="btn btn-square btn-ghost" @click="handleCancelEditOrder">
          <span class="i-mingcute-close-fill text-3xl" />
        </button>
        <button class="btn btn-square btn-ghost" @click="handleSaveYardOrder">
          <span class="i-mingcute-save-2-line text-3xl" />
        </button>
      </template>
      <button v-else class="btn btn-square btn-ghost" @click="isEditOrderMode = true">
        <span class="i-mingcute-transfer-4-line text-3xl" />
      </button>
      <button v-if="isAdmin" class="btn btn-square btn-ghost" @click="isNewYardOpen = true">
        <span class="i-mingcute-add-fill text-3xl" />
      </button>
    </AppHeader>

    <div class="mx-5 mb-6 flex items-start gap-2 rounded-lg bg-secondary bg-opacity-20 px-4 py-3">
      <span class="i-mingcute-information-fill flex-shrink-0 text-xl text-secondary" />
      <p>Activa la edición de orden y usa las flechas para modificar el orden de patios</p>
    </div>

    <YardList
      v-if="editingYardOrder"
      v-model="editingYardOrder.yardOrder"
      :show-delete="isAdmin"
      :edit-mode="isEditOrderMode"
      @delete="handleDeleteYard"
    />

    <BottomDrawer class="bg-base-200" size="small" v-model="isNewYardOpen" v-slot="{ close }">
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
