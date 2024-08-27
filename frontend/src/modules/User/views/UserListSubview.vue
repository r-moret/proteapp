<script setup lang="ts">
import { useUserStore } from '@/store/UserStore'
import { storeToRefs } from 'pinia'
import { onBeforeMount } from 'vue'
import UserList from '@/modules/User/components/UserList.vue'
import { usePersonStore } from '@/store/PersonStore'
import { useRouter } from 'vue-router'
import type { UserInfo } from '@/modules/User/declarations'

const router = useRouter()

const personStore = usePersonStore()
const userStore = useUserStore()
const { userList } = storeToRefs(userStore)

function navigateEdit(user: UserInfo) {
  router.push({ name: 'people.volunteers.edit', params: { id: user.id } })
}

onBeforeMount(async () => {
  await personStore.fetchPeople()
  await userStore.fetchUsers()
})
</script>

<template>
  <main class="flex flex-col">
    <UserList class="px-1" :user-list="userList" @click-user="navigateEdit" />
  </main>
</template>
