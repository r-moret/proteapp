<script setup lang="ts">
import TextInput from '@/components/TextInput.vue'
import { onBeforeMount, ref } from 'vue'
import { useAuthStore } from '@/store/AuthStore'
import { storeToRefs } from 'pinia'
import { useToastNotifications } from '@/composable/useToastNotifications'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const authStore = useAuthStore()
const { loggedUser, authError, isLoading, isAuthenticated } = storeToRefs(authStore)

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification } = useToastNotifications(notificationsRef)

const email = ref<string>()
const password = ref<string>()

async function handleSubmitLogin() {
  if (!email.value || !password.value) return

  await authStore.login(email.value, password.value)

  if (authError.value) {
    showErrorNotification(authError.value)
    email.value = undefined
    password.value = undefined
  } else {
    router.push({ name: 'animals' })
  }
}

onBeforeMount(() => {
  if (isAuthenticated.value && loggedUser.value) router.push({ name: 'animals' })
})
</script>

<template>
  <main class="flex flex-col items-center pb-32 pt-52">
    <ToastNotifications ref="notificationsRef" />

    <div class="flex h-full w-4/5 flex-col">
      <h1 class="mb-16 w-full text-center text-5xl font-bold">
        Prote<span class="text-secondary">app</span>
      </h1>
      <div class="flex flex-col items-center gap-6">
        <h2 class="text-2xl font-semibold">Iniciar sesión</h2>
        <form class="flex w-full flex-col items-center gap-4" @submit.prevent="handleSubmitLogin">
          <TextInput
            type="email"
            name="login-email"
            placeholder="Correo electrónico"
            v-model="email"
          >
            <template #icon>
              <span class="i-mingcute-user-3-fill text-2xl text-secondary" />
            </template>
          </TextInput>
          <TextInput
            type="password"
            name="login-password"
            placeholder="Contraseña"
            v-model="password"
          >
            <template #icon>
              <span class="i-mingcute-key-2-fill text-2xl text-secondary" />
            </template>
          </TextInput>
          <button
            class="mt-4 w-fit rounded-lg bg-secondary px-8 py-2 font-semibold text-secondary-content"
          >
            Entrar
          </button>
        </form>
      </div>

      <div v-if="isLoading" class="mt-20 flex justify-center">
        <span class="loading loading-bars loading-lg text-secondary" />
      </div>

      <p class="mt-auto font-semibold">
        ¿Has olvidado tu contraseña o no tienes una cuenta?
        <span class="text-secondary">Contacta con administración.</span>
      </p>
    </div>
  </main>
</template>
