<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { computed, ref, onBeforeMount } from 'vue'
import { ZodError } from 'zod'

import { usePersonStore } from '@/store/PersonStore'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { EditPersonAdapter } from '@/modules/Person/adapters'

import PersonList from '@/modules/Person/components/PersonList.vue'
import ToastNotifications from '@/components/ToastNotifications.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import TextInput from '@/components/TextInput.vue'

import type { EditPerson } from '../declarations'

const route = useRoute()
const router = useRouter()

const personStore = usePersonStore()
const { personList } = storeToRefs(personStore)

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const isNewPersonOpen = computed(() => route.name === 'people.create')

const newPersonForm = ref<HTMLFormElement | null>(null)
const newPerson = ref<EditPerson>()

function handleCloseNewPersonDrawer() {
  router.push({ name: 'people' })
}

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
  <ToastNotifications ref="notificationsRef" />

  <PersonList class="px-1" :person-list="personList"></PersonList>

  <BottomDrawer
    class="bg-base-200"
    size="big"
    :model-value="isNewPersonOpen"
    @update:model-value="handleCloseNewPersonDrawer"
    v-slot="{ close }"
  >
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
</template>
