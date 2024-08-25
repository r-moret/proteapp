<script setup lang="ts">
import { useUserStore } from '@/store/UserStore'
import { storeToRefs } from 'pinia'
import { onBeforeMount } from 'vue'
import UserList from '@/modules/User/components/UserList.vue'
import { usePersonStore } from '@/store/PersonStore'

const personStore = usePersonStore()
const userStore = useUserStore()
const { userList } = storeToRefs(userStore)

onBeforeMount(async () => {
  await personStore.fetchPeople()
  await userStore.fetchUsers()
})
</script>

<template>
  <main class="flex flex-col">
    <UserList class="px-1" :user-list="userList"></UserList>
  </main>
</template>
