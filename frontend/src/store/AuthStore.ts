import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useJwt } from '@vueuse/integrations/useJwt'
import { crudUser as crudUserApi } from '@/modules/Inform/api'
import { UserAdapter } from '@/modules/User/adapters'
import type { User } from '@/modules/Inform/declarations'

export const useAuthStore = defineStore('AuthStore', () => {
  const token = ref<string>()
  const loggedUser = ref<User>()
  const isAuthenticated = ref(false)
  const isLoading = ref(false)

  const authError = ref<string>()

  async function login(username: string, password: string) {
    isLoading.value = true

    const body = new FormData()

    body.set('username', username)
    body.set('password', password)

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/auth/token`, {
      method: 'POST',
      body
    })
      .then((res) => {
        authError.value = undefined

        if (!res.ok) return Promise.reject(res)
        return res.json()
      })
      .then((json) => (token.value = json.access_token))
      .catch((res) => {
        if (res.status === 401)
          authError.value = 'Credenciales inválidas, por favor, prueba de nuevo.'
        else authError.value = 'Lo siento, un error inesperado ocurrió intentando iniciar sesión.'

        isLoading.value = false
      })

    if (!token.value) return

    const { payload } = useJwt(token.value)
    const authUserId = payload.value?.sub

    if (!authUserId) {
      authError.value = 'Lo siento, no es posible encontrar tu usuario.'
      isLoading.value = false
      return
    }

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}/${authUserId}`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
      .then((res) => {
        if (!res.ok) return Promise.reject()
        return res.json()
      })
      .then(UserAdapter)
      .then((user) => {
        loggedUser.value = user
        isAuthenticated.value = true
      })
      .catch(() => {
        authError.value = 'Lo siento, un error inesperado ocurrió intentando obtener tu usuario.'
        isLoading.value = false
      })

    isLoading.value = false
  }

  return {
    token,
    loggedUser,
    isAuthenticated,
    isLoading,
    authError,

    login
  }
})
