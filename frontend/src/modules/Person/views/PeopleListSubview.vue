<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { computed, ref, onBeforeMount } from 'vue'
import { ZodError } from 'zod'

import { usePersonStore } from '@/store/PersonStore'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { EditPersonAdapter } from '@/modules/Person/adapters'
import { useParams } from '@/composable/useParams'

import PersonList from '@/modules/Person/components/PersonList.vue'
import ToastNotifications from '@/components/ToastNotifications.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import PersonEditor from '@/modules/Person/components/PersonEditor.vue'

import type { EditPerson, Person } from '@/modules/Person/declarations'

const route = useRoute()
const router = useRouter()
const routeParams = useParams<{
  id?: string
}>()

const personStore = usePersonStore()
const { personList, personDetails } = storeToRefs(personStore)

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const isEditMode = computed(() => !!routeParams.value.id)
const isEditingPersonOpen = computed(
  () => route.name === 'people.create' || route.name === 'people.edit'
)

const editingPerson = ref<EditPerson>()

function handleCloseNewPersonDrawer() {
  editingPerson.value = {
    name: '',
    firstSurname: '',
    phone: '',
    email: ''
  }
  router.push({ name: 'people' })
}

async function handleAddPerson(callback: () => void) {
  if (!editingPerson.value) return

  try {
    EditPersonAdapter(editingPerson.value)

    if (isEditMode.value && routeParams.value.id) {
      await personStore.updatePerson(routeParams.value.id, editingPerson.value)
      showSuccessNotification('Persona editada correctamente.')
    } else {
      await personStore.createPerson(editingPerson.value)
      showSuccessNotification('Persona añadida correctamente.')
    }

    callback()
    editingPerson.value = {
      name: '',
      firstSurname: '',
      phone: '',
      email: ''
    }
  } catch (error) {
    if (error instanceof ZodError) {
      showErrorNotification(
        'Faltan datos para guardar la persona o están en un formato incorrecto.'
      )
    } else {
      showErrorNotification('Ha ocurrido un error, prueba otra vez.')
    }
  }
}

function navigateEdit(person: Person) {
  editingPerson.value = person
  router.push({ name: 'people.edit', params: { id: person.id } })
}

onBeforeMount(async () => {
  await personStore.fetchPeople()

  if (isEditMode.value) {
    await personStore.fetchPerson(routeParams.value.id!)

    if (!personDetails.value) {
      showErrorNotification('No se encontró ninguna persona.')
      router.push({ name: 'people' })
      return
    }

    editingPerson.value = { ...personDetails.value }
  } else {
    editingPerson.value = {
      name: '',
      firstSurname: '',
      phone: '',
      email: ''
    }
  }
})
</script>

<template>
  <ToastNotifications ref="notificationsRef" />

  <PersonList class="px-1" :person-list="personList" @click-person="navigateEdit" />

  <BottomDrawer
    class="bg-base-200"
    size="big"
    :model-value="isEditingPersonOpen"
    @update:model-value="handleCloseNewPersonDrawer"
    v-slot="{ close }"
  >
    <div class="flex h-full flex-col gap-5">
      <h1 class="text-3xl font-semibold">{{ isEditMode ? 'Editar persona' : 'Nueva persona' }}</h1>
      <form
        v-if="editingPerson"
        class="flex h-full flex-col gap-6 pb-10"
        @submit.prevent="handleAddPerson(close)"
      >
        <PersonEditor v-model="editingPerson" :embedded="false" />
        <button
          class="mt-auto w-fit self-center rounded-lg bg-secondary px-10 py-3 text-xl font-semibold text-white"
        >
          {{ isEditMode ? 'Guardar' : 'Añadir' }}
        </button>
      </form>
    </div>
  </BottomDrawer>
</template>
