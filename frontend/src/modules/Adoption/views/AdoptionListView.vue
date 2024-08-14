<script setup lang="ts">
import AppHeader from '@/skeleton/AppHeader.vue'
import AdoptionList from '@/modules/Adoption/components/AdoptionList.vue'
import { useAdoptionStore } from '@/store/AdoptionStore'
import { storeToRefs } from 'pinia'
import { onBeforeMount, ref } from 'vue'
import type { EditAdoption } from '../declarations'
import { EditAdoptionAdapter } from '@/modules/Adoption/adapters'
import ToastNotifications from '@/components/ToastNotifications.vue'
const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)
import { ZodError } from 'zod'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { addDay } from '@formkit/tempo'
import BottomDrawer from '@/components/BottomDrawer.vue'

const adoptionStore = useAdoptionStore()
const newAdoption = ref<EditAdoption>()
const { adoptionList } = storeToRefs(adoptionStore)
const newAdoptionForm = ref<HTMLFormElement | null>(null)

onBeforeMount(async () => {
  await adoptionStore.fetchAdoptions()
  newAdoption.value = {
    person: '',
    animal: '',
    registerDate: addDay(new Date()),
    foster: false
  }
})
const newAdoptionOpen = ref(false)

async function handleAddAdoption(closeDrawer: () => void) {
  if (!newAdoption.value) return

  try {
    newAdoption.value.registerDate = new Date(
      newAdoption.value.registerDate.getFullYear(),
      newAdoption.value.registerDate.getMonth(),
      newAdoption.value.registerDate.getDate()
    )
    EditAdoptionAdapter(newAdoption.value)

    await adoptionStore.createAdoption(newAdoption.value)
    showSuccessNotification('Adopción añadida correctamente.')

    newAdoptionForm.value?.reset()
    newAdoption.value = {
      registerDate: addDay(new Date()),
      foster: false,
      animal: '',
      person: ''
    }
    closeDrawer()
  } catch (error) {
    if (error instanceof ZodError) {
      showErrorNotification('Parece que hay un error con los datos de la adopción.')
    } else {
      showErrorNotification('Ha ocurrido un error, prueba otra vez.')
    }
  }
}
</script>

<template>
  <main class="flex flex-col">
    <AppHeader left="back" title="Adopciones">
      <button class="btn btn-square btn-ghost" @click="newAdoptionOpen = true">
        <span class="i-mingcute-add-fill text-3xl" />
      </button>
    </AppHeader>

    <AdoptionList :adoption-list="adoptionList"></AdoptionList>
    <BottomDrawer class="bg-base-200" size="small" v-model="newAdoptionOpen" v-slot="{ close }">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Nuevo seguimiento</h1>
        <form
          v-if="newAdoption"
          ref="newAdoptionForm"
          class="flex h-full flex-col gap-6 pb-10"
          @submit.prevent="handleAddAdoption(close)"
        >
          <di v class="flex flex-col gap-2">
            <label class="font-semibold" for="new-adoption-description"> Animal a adoptar </label>
            <TextInput
              name="new-monitoring-description"
              placeholder="ej. Adaptado correctamente"
              v-model="newAdoption.animal"
            />
          </di>
          <div class="flex flex-col gap-2">
            <label class="font-semibold" for="">Fecha de adopción</label>
            <DateInputS
              :include-time="false"
              placeholder="ej. 23 de mayo de 2023"
              v-model="newAdoption.registerDate"
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
