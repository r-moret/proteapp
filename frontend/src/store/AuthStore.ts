import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useJwt } from '@vueuse/integrations/useJwt'
import { crudUser as crudUserApi } from '@/modules/Inform/api'
import { UserAdapter } from '@/modules/User/adapters'
import type { User } from '@/modules/User/declarations'
import type { JwtPayload } from 'jwt-decode'

interface JwtPayloadWithScopes extends JwtPayload {
  scopes?: string[]
}

export const useAuthStore = defineStore('AuthStore', () => {
  const token = ref<string>()
  const loggedUser = ref<User>()
  const isAdmin = ref(false)
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

    const { payload } = useJwt<JwtPayloadWithScopes>(token.value)
    const authUserId = payload.value?.sub
    const authUserRoles = payload.value?.scopes
    console.log(payload.value)

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

    isAdmin.value = authUserRoles?.includes('admin') ?? false

    isLoading.value = false
  }

  return {
    token,
    loggedUser,
    isAdmin,
    isAuthenticated,
    isLoading,
    authError,

    login
  }
})
