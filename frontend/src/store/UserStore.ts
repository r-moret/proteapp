import { ref } from 'vue'
import { defineStore } from 'pinia'
import { crudUser as crudUserApi, listUser as listUserApi } from '@/modules/Inform/api'
import type { UserInfo, User } from '@/modules/Inform/declarations'
import { UserInfoAdapter, UserAdapter } from '@/modules/Inform/adapters'

export const useUserStore = defineStore('UserStore', () => {
  const loggedUser = ref<User>()
  const userList = ref<UserInfo[]>([])
  const userDetails = ref<User>()
  const isLoading = ref(false)

  async function loginUser() {
    const loggedUserId = '01J3DSAAMJCCXJNB7M2XZGVEPW' // TODO

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}/${loggedUserId}`)
      .then((res) => res.json())
      .then(UserAdapter)
      .then((user) => (loggedUser.value = user))
  }

  async function fetchUsers() {
    isLoading.value = true

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${listUserApi}`)
      .then((res) => res.json())
      .then((json) => json.map(UserInfoAdapter))
      .then((users) => (userList.value = users))

    isLoading.value = false
  }

  async function fetchUser(id: string) {
    isLoading.value = true

    await fetch(`${import.meta.env.VITE_BACKEND_URL}/${crudUserApi}/${id}`)
      .then((res) => res.json())
      .then(UserAdapter)
      .then((user) => (userDetails.value = user))

    isLoading.value = false
  }

  return {
    loggedUser,
    userDetails,
    userList,
    isLoading,
    loginUser,
    fetchUser,
    fetchUsers
  }
})
