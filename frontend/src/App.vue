<script setup lang="ts">
import NavigationBar from '@/skeleton/NavigationBar.vue'
import { RouterView } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from './store/AuthStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)

const router = useRouter()

router.beforeEach((to) => {
  if (!isAuthenticated.value && to.name !== 'login') return { name: 'login' }
})
</script>

<template>
  <div class="h-full min-h-screen bg-base-200">
    <RouterView :class="['h-screen', { 'pb-16': isAuthenticated }]" />
  </div>
  <NavigationBar v-if="isAuthenticated" class="h-16" />
</template>
