import { ref } from 'vue'
import { defineStore } from 'pinia'
import { crudUser as crudUserApi, listUser as listUserApi } from '@/modules/Inform/api'
import type { UserInfo, User } from '@/modules/Inform/declarations'
import { UserInfoAdapter, UserAdapter } from '@/modules/Inform/adapters'
import type { EditUser } from '@/modules/User/declarations'
import { authFetch } from '@/composable/useAuthFetch'

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

  async function createUser(user: EditUser) {
    await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}`, {
      method: 'post',
      body: JSON.stringify(user),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(async (data) => {
      if (!data.ok) {
        throw Error(`Error backend response: ${await data.json()}`)
      }
    })
    await fetchUsers()
  }

  return {
    userDetails,
    userList,
    isLoading,
    fetchUser,
    fetchUsers,
    deleteUser,
    createUser
  }
})
