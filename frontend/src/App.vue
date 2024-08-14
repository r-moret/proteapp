<script setup lang="ts">
import NavigationBar from '@/skeleton/NavigationBar.vue'
import { onBeforeMount } from 'vue'
import { RouterView } from 'vue-router'
import { useUserStore } from '@/store/UserStore'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const { loggedUser } = storeToRefs(userStore)

onBeforeMount(async () => {
  await userStore.loginUser()
})
</script>

<template>
  <div class="h-full min-h-screen bg-base-200">
    <RouterView v-if="loggedUser" class="h-screen pb-16" />
  </div>
  <NavigationBar class="h-16" />
</template>
