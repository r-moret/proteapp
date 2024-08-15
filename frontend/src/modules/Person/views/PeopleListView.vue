<script setup lang="ts">
import AppHeader from '@/skeleton/AppHeader.vue'
import { onBeforeMount, ref } from 'vue'
import { usePersonStore } from '@/store/PersonStore'
import { storeToRefs } from 'pinia'
import PersonList from '@/modules/Person/components/PersonList.vue'
import { EditPersonAdapter } from '@/modules/Person/adapters'
import type { EditPerson } from '../declarations'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { ZodError } from 'zod'
import BottomDrawer from '@/components/BottomDrawer.vue'
import TextInput from '@/components/TextInput.vue'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)

const personStore = usePersonStore()
const { personList } = storeToRefs(personStore)

const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)
const newPersonForm = ref<HTMLFormElement | null>(null)
const newPersonOpen = ref(false)
const newPerson = ref<EditPerson>()

async function handleAddPerson(callback: () => void) {
  if (!newPerson.value) return

  try {
    newPerson.value.phone = '+34' + newPerson.value.phone
    EditPersonAdapter(newPerson.value)
    await personStore.createPerson(newPerson.value)
    showSuccessNotification('Persona añadida correctamente.')

    newPersonForm.value?.reset()
    newPerson.value = {
      name: '',
      firstSurname: '',
      phone: ''
    }
    callback()
  } catch (error) {
    newPersonForm.value?.reset()
    newPerson.value = {
      name: '',
      firstSurname: '',
      phone: ''
    }
    if (error instanceof ZodError) {
      showErrorNotification('Parece que hay un error con los datos de la persona.')
    } else {
      showErrorNotification('Ha ocurrido un error, prueba otra vez.')
    }
  }
}

onBeforeMount(async () => {
  await personStore.fetchPeople()
  newPerson.value = {
    name: '',
    firstSurname: '',
    phone: ''
  }
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificationsRef" />
    <AppHeader left="profile" title="Personas">
      <button class="btn btn-square btn-ghost" @click="newPersonOpen = true">
        <span class="i-mingcute-add-fill text-3xl" />
      </button>
    </AppHeader>
    <PersonList :person-list="personList"></PersonList>

    <BottomDrawer class="bg-base-200" size="small" v-model="newPersonOpen" v-slot="{ close }">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Nueva persona</h1>
        <form
          v-if="newPerson"
          ref="newPersonForm"
          class="flex h-full flex-col gap-6 pb-10"
          @submit.prevent="handleAddPerson(close)"
        >
          <div v class="flex flex-col gap-2">
            <label class="font-semibold" for="new-person-name"> Nombre *</label>
            <TextInput
              name="new-person-name"
              placeholder="ej. Juan"
              v-model="newPerson.name"
              :req="true"
            />
          </div>
          <div v class="flex flex-col gap-2">
            <label class="font-semibold" for="new-person-surname"> Primer apellido *</label>
            <TextInput
              name="new-person-surname"
              placeholder="ej. Pérez"
              v-model="newPerson.firstSurname"
              :req="true"
            />
          </div>
          <div v class="flex flex-col gap-2">
            <label class="font-semibold" for="new-person-second-surname"> Segundo apellido </label>
            <TextInput
              name="new-person-second-surname"
              placeholder="ej. Machado"
              v-model="newPerson.secondSurname"
            />
          </div>

          <div v class="flex flex-col gap-2">
            <label class="font-semibold" for="new-person-phone"> Teléfono * </label>
            <TextInput
              :req="true"
              name="new-person-phone"
              placeholder=""
              v-model="newPerson.phone"
              required
            />
          </div>

          <div v class="flex flex-col gap-2">
            <label class="font-semibold" for="new-person-email"> Email </label>
            <TextInput name="new-person-email" placeholder="" v-model="newPerson.email" />
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
