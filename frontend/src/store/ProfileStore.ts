import { defineStore } from 'pinia'
import { EditUserAdapter } from '@/modules/User/adapters'
import type { EnrichedEditUser } from '@/modules/User/declarations'
import { authFetch } from '@/composable/useAuthFetch'
import type { EditPerson } from '@/modules/Person/declarations'
import { useAuthStore } from '@/store/AuthStore'

const authStore = useAuthStore()

export const useProfileStore = defineStore('ProfileStore', () => {
  async function updateProfile(enrichedUser: EnrichedEditUser) {
    const user = EditUserAdapter({ ...enrichedUser, person: enrichedUser.person.id })

    if (user.image && new URL(user.image).protocol !== 'blob:') return

    if (!user.image) {
      await authFetch(`${import.meta.env.VITE_BACKEND_URL}/profile/image`, {
        method: 'delete'
      })
      await authStore.fetchLoggedUser()
      return
    }

    const image = await fetch(user.image)
    const imageFile = await image.blob()

    const body = new FormData()
    body.set('image', imageFile)

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/profile/image`, {
      method: 'post',
      body
    })

    await authStore.fetchLoggedUser()
  }

  async function updateProfilePerson(person: EditPerson) {
    const response = await authFetch(`${import.meta.env.VITE_BACKEND_URL}/profile/person`, {
      method: 'put',
      body: JSON.stringify(person),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) throw Error(`Error backend response: ${await response.json()}`)

    await authStore.fetchLoggedUser()
  }

  return {
    updateProfile,
    updateProfilePerson
  }
})
