<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import { useProfileStore } from '@/store/ProfileStore'
import { useAuthStore } from '@/store/AuthStore'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import AppHeader from '@/skeleton/AppHeader.vue'
import UserEditor from '@/modules/User/components/UserEditor.vue'
import type { EnrichedEditUser } from '@/modules/User/declarations'
import { EnrichedEditUserAdapter } from '@/modules/User/adapters'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { useToastNotifications } from '@/composable/useToastNotifications'

const router = useRouter()
const profileStore = useProfileStore()
const { loggedUser } = storeToRefs(useAuthStore())

const editingProfile = ref<EnrichedEditUser>()

const notificiationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificiationsRef)

async function handleSaveVolunteer() {
  try {
    EnrichedEditUserAdapter(editingProfile.value)
  } catch (error) {
    showErrorNotification(
      'Faltan datos para poder guardar el voluntario o están en un formato incorrecto.'
    )
    return
  }

  try {
    await profileStore.updateProfilePerson(editingProfile.value!.person)
    await profileStore.updateProfile(editingProfile.value!)

    showSuccessNotification('Perfil editado correctamente.')
  } catch (error) {
    showErrorNotification(
      'Parece que un error inesperado ocurrió guardando el voluntario, por favor prueba de nuevo.'
    )
    return
  }
}

onBeforeMount(() => {
  if (!loggedUser.value) {
    router.push({ name: 'home' })
    return
  }

  editingProfile.value = { ...loggedUser.value }
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificiationsRef" />

    <AppHeader left="back" title="Editar perfil">
      <button class="btn btn-square btn-ghost" @click="handleSaveVolunteer">
        <span class="i-mingcute-save-2-line text-3xl" />
      </button>
    </AppHeader>

    <section class="min-h-0 w-full flex-grow overflow-y-auto px-6 pb-8">
      <UserEditor v-if="editingProfile" v-model="editingProfile" person="editor" />
    </section>
  </main>
</template>
