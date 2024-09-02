import { ref } from 'vue'
import { defineStore } from 'pinia'
import { crudUser as crudUserApi, listUser as listUserApi } from '@/modules/Inform/api'
import type { UserInfo, User } from '@/modules/User/declarations'
import { UserInfoAdapter, UserAdapter, EditUserAdapter } from '@/modules/User/adapters'
import type { EnrichedEditUser } from '@/modules/User/declarations'
import { authFetch } from '@/composable/useAuthFetch'
import { omit } from 'lodash'

export const useUserStore = defineStore('UserStore', () => {
  const userList = ref<UserInfo[]>([])
  const userDetails = ref<User>()
  const isLoading = ref(false)

  async function fetchUsers() {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${listUserApi}`)
      .then((res) => res.json())
      .then((json) => json.map(UserInfoAdapter))
      .then((users) => (userList.value = users))

    isLoading.value = false
  }

  async function fetchUser(id: string) {
    isLoading.value = true

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}/${id}`)
      .then((res) => res.json())
      .then(UserAdapter)
      .then((user) => (userDetails.value = user))

    isLoading.value = false
  }

  async function deleteUser(userId: string) {
    if (!userList.value || !userList.value.map((user) => user.id).includes(userId)) {
      throw Error(
        'Cannot delete an user that belongs to an user different than the one that is loaded'
      )
    }

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}/${userId}`, {
      method: 'delete'
    })
    userList.value = userList.value.filter((user) => user.id !== userId)
  }

  async function createUser(enrichedUser: EnrichedEditUser) {
    const user = EditUserAdapter({ ...enrichedUser, person: enrichedUser.person.id })

    const response = await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}`, {
      method: 'post',
      body: JSON.stringify(omit(user, 'image')),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) throw Error(`Error backend response: ${await response.json()}`)
    if (!user.image) return
    const createdUser = UserAdapter(await response.json())

    const image = await fetch(user.image)
    const imageFile = await image.blob()

    const body = new FormData()
    body.set('image', imageFile)

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}/${createdUser.id}/image`, {
      method: 'post',
      body
    })

    await fetchUsers()
  }

  async function updateUser(userId: string, enrichedUser: EnrichedEditUser) {
    const user = EditUserAdapter({ ...enrichedUser, person: enrichedUser.person.id })

    const response = await authFetch(
      `${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}/${userId}`,
      {
        method: 'put',
        body: JSON.stringify(omit(user, 'image')),
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) throw Error(`Error backend response: ${await response.json()}`)
    if (user.image && new URL(user.image).protocol !== 'blob:') return

    if (!user.image) {
      await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}/${userId}/image`, {
        method: 'delete'
      })
      return
    }

    const image = await fetch(user.image)
    const imageFile = await image.blob()

    const body = new FormData()
    body.set('image', imageFile)

    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}/${userId}/image`, {
      method: 'post',
      body
    })
  }

  return {
    userDetails,
    userList,
    isLoading,
    fetchUser,
    fetchUsers,
    deleteUser,
    createUser,
    updateUser
  }
})
