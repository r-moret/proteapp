<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import { useParams } from '@/composable/useParams'
import ImagePicker from '@/components/ImagePicker.vue'
import type { EnrichedEditUser } from '@/modules/User/declarations'
import { EnrichedEditUserAdapter } from '@/modules/User/adapters'
import { useUserStore } from '@/store/UserStore'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import PersonSelector from '@/modules/Adoption/components/PersonSelector.vue'
import PersonEditor from '@/modules/Person/components/PersonEditor.vue'
import { usePersonStore } from '@/store/PersonStore'

const params = useParams<{
  id?: string
}>()

const personStore = usePersonStore()

const userStore = useUserStore()
const { userDetails } = storeToRefs(userStore)

const router = useRouter()

const notificiationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification } = useToastNotifications(notificiationsRef)

const isEditMode = ref(!!params.value.id)
const editingVolunteer = ref<Partial<EnrichedEditUser>>()

async function handleSaveVolunteer() {
  try {
    EnrichedEditUserAdapter(editingVolunteer.value)
  } catch (error) {
    showErrorNotification(
      'Faltan datos para poder guardar el voluntario o están en un formato incorrecto.'
    )
    return
  }

  try {
    if (isEditMode.value && params.value.id) {
      await personStore.updatePerson(
        editingVolunteer.value!.person!.id,
        editingVolunteer.value!.person!
      )
      await userStore.updateUser(params.value.id, editingVolunteer.value as EnrichedEditUser)
    } else {
      await userStore.createUser(editingVolunteer.value as EnrichedEditUser)
    }

    router.push({ name: 'people.volunteers' })
  } catch (error) {
    showErrorNotification(
      'Parece que un error inesperado ocurrió guardando el voluntario, por favor prueba de nuevo.'
    )
    return
  }
}

onBeforeMount(async () => {
  if (isEditMode.value) {
    await userStore.fetchUser(params.value.id!)

    if (!userDetails.value) {
      showErrorNotification('No se encontró ningún voluntario.')
      router.push({ name: 'people.volunteers' })
      return
    }

    editingVolunteer.value = {
      ...userDetails.value
    }
  } else {
    editingVolunteer.value = {
      person: undefined,
      active: true,
      veteran: false,
      image: undefined
    }
  }
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificiationsRef" />

    <AppHeader left="back" :title="isEditMode ? 'Editar voluntario' : 'Crear voluntario'">
      <button class="btn btn-square btn-ghost" @click="handleSaveVolunteer">
        <span class="i-mingcute-save-2-line text-3xl" />
      </button>
    </AppHeader>

    <section class="min-h-0 w-full flex-grow overflow-y-auto px-6 pb-8">
      <div v-if="editingVolunteer" class="flex flex-col gap-4">
        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Imagen</h2>
          <ImagePicker v-model="editingVolunteer.image" class="px-2" />
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Persona</h2>
          <PersonEditor v-if="isEditMode" v-model="editingVolunteer.person" :embedded="true" />
          <PersonSelector v-else v-model="editingVolunteer.person" />
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Detalles</h2>
          <label class="label gap-2">
            <input
              type="checkbox"
              class="checkbox-secondary checkbox"
              v-model="editingVolunteer.veteran"
            />
            <span class="label-text w-full text-start font-semibold"> Voluntario veterano </span>
          </label>
        </div>
      </div>
    </section>
  </main>
</template>
