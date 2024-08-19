<script setup lang="ts">
import { useUserStore } from '@/store/UserStore'
import { storeToRefs } from 'pinia'
import { onBeforeMount, ref } from 'vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import UserList from '@/modules/User/components/UserList.vue'
const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)
import ToastNotifications from '@/components/ToastNotifications.vue'
import type { EditUser } from '../declarations'
import { EditUserAdapter } from '@/modules/User/adapters'
import type { Person } from '@/modules/Person/declarations'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { ZodError } from 'zod'
import PersonSelector from '@/modules/Adoption/components/PersonSelector.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import { usePersonStore } from '@/store/PersonStore'

const personStore = usePersonStore()
const userStore = useUserStore()
const { userList } = storeToRefs(userStore)
const newUserPerson = ref<Person>()

const newUser = ref<EditUser>({
  person: '',
  image: null,
  active: true,
  veteran: false,
  password: ''
})
const newUserOpen = ref(false)

// async function handleFileUpload(event: Event) {
//   try {
//     const input = event.target as HTMLInputElement
//     if (!input.files || input.files.length === 0) return

//     const file = input.files[0]
//     newUser.value.image = file
//   } catch (error) {
//     console.error('Error en la subida de la imagen:', error)
//     showErrorNotification('Ha ocurrido un error al subir la imagen, prueba otra vez.')
//   }
// }

async function handleAddUser(closeDrawer: () => void) {
  if (!newUser.value || !newUserPerson.value) return

  try {
    newUser.value.person = newUserPerson.value.id

    EditUserAdapter(newUser.value)

    await userStore.createUser(newUser.value)
    showSuccessNotification('Usuario añadido correctamente.')

    newUser.value = {
      person: '',
      image: null,
      active: true,
      veteran: false,
      password: ''
    }
    newUserPerson.value = undefined
    closeDrawer()
  } catch (error) {
    if (error instanceof ZodError) {
      showErrorNotification('Parece que hay un error con los datos del usuario.')
    } else {
      showErrorNotification('Ha ocurrido un error, prueba otra vez.')
    }
  }
}

onBeforeMount(async () => {
  await personStore.fetchPeople()
  await userStore.fetchUsers()
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificationsRef" />
    <AppHeader left="profile" title="Usuarios">
      <button class="btn btn-square btn-ghost" @click="newUserOpen = true">
        <span class="i-mingcute-add-fill text-3xl" />
      </button>
    </AppHeader>

    <section class="min-h-0 w-full flex-grow overflow-y-auto px-4">
      <UserList :user-list="userList"></UserList>
    </section>

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
            <!--Esto es para seleccionar imagen, borrar cuando ya no sea necesario-->
            <!-- <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Imagen de Usuario</h2>
              <input type="file" @change="handleFileUpload" accept="image/*" class="file-input" />
            </section> -->
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
  </main>
</template>
