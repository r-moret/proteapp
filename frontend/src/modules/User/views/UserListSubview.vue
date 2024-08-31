<script setup lang="ts">
import { useUserStore } from '@/store/UserStore'
import { storeToRefs } from 'pinia'
import { onBeforeMount } from 'vue'
import UserList from '@/modules/User/components/UserList.vue'
import { usePersonStore } from '@/store/PersonStore'
import { useRouter } from 'vue-router'
import type { UserInfo } from '@/modules/User/declarations'
import { useAuthStore } from '@/store/AuthStore'

const router = useRouter()

const authStore = useAuthStore()
const personStore = usePersonStore()
const userStore = useUserStore()

const { userList } = storeToRefs(userStore)
const { isAdmin } = storeToRefs(authStore)

function navigateEdit(user: UserInfo) {
  if (!isAdmin.value) return
  router.push({ name: 'people.volunteers.edit', params: { id: user.id } })
}

onBeforeMount(async () => {
  await personStore.fetchPeople()
  await userStore.fetchUsers()
})
</script>

<template>
  <main class="flex flex-col">
    <UserList
      class="px-1"
      :user-list="userList"
      :show-delete="isAdmin"
      @click-user="navigateEdit"
    />
  </main>
</template>
