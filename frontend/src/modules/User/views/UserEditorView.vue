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

const params = useParams<{
  id?: string
}>()

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
          <h2 class="text-xl font-semibold">Persona</h2>
          <PersonSelector v-model="editingVolunteer.person" />
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Imagen</h2>
          <ImagePicker v-model="editingVolunteer.image" class="px-2" />
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

<!-- <script setup lang="ts">
// const newUserPerson = ref<Person>()

// async function handleAddUser(closeDrawer: () => void) {
//   if (!newUser.value || !newUserPerson.value) return

//   try {
//     newUser.value.person = newUserPerson.value.id

//     EditUserAdapter(newUser.value)

//     await userStore.createUser(newUser.value)
//     showSuccessNotification('Usuario añadido correctamente.')

//     newUser.value = {
//       person: '',
//       image: null,
//       active: true,
//       veteran: false,
//       password: ''
//     }
//     newUserPerson.value = undefined
//     closeDrawer()
//   } catch (error) {
//     if (error instanceof ZodError) {
//       showErrorNotification('Parece que hay un error con los datos del usuario.')
//     } else {
//       showErrorNotification('Ha ocurrido un error, prueba otra vez.')
//     }
//   }
// }
</script> -->

<!-- <template>
  Editor
  <BottomDrawer class="bg-base-200" size="small" v-model="newUserOpen" v-slot="{ close }">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Nuevo usuario</h1>
        <div v-if="newUser" class="flex h-full flex-col gap-6 pb-10">
          <div class="flex flex-col gap-2">
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Persona</h2>
              <PersonSelector v-model="newUserPerson" />
            </section>
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Veterano</h2>
              <div class="flex items-center gap-3">
                <label class="text-lg font-medium" for="veteranToggle">
                  {{ newUser.veteran ? 'Sí' : 'No' }}
                </label>
                <input
                  type="checkbox"
                  id="veteranToggle"
                  v-model="newUser.veteran"
                  class="toggle bg-secondary"
                />
              </div>
            </section>
          </div>
          <button
            @click="handleAddUser(close)"
            class="w-fit self-center rounded-lg bg-secondary px-10 py-3 text-xl font-semibold text-white"
          >
            Añadir
          </button>
        </div>
      </div>
    </BottomDrawer>
</template> -->
