import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { fakeUser } from '@/fakes'
import { sleep } from '@/utils'
import type { User } from '@/types'

export const useUserStore = defineStore('UserStore', () => {
  const user = ref<User>({
    name: '',
    surnames: '',
    email: '',
    isVeteran: false
  })
  const isLoading = ref<boolean>(false)

  const fullname = computed(() => `${user.value.name} ${user.value.surnames}`)

  async function fetchUser() {
    isLoading.value = true

    await sleep(3000)
    user.value = fakeUser
    isLoading.value = false
  }

  return {
    user,
    fullname,
    isLoading,
    fetchUser
  }
})
