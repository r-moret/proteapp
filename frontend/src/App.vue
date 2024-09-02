<script setup lang="ts">
import NavigationBar from '@/skeleton/NavigationBar.vue'
import { RouterView } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from './store/AuthStore'
import { useRouter } from 'vue-router'
import { RestrictedRoutes } from '@/config/RestrictedRoutes'

const authStore = useAuthStore()
const { isAuthenticated, isAdmin } = storeToRefs(authStore)

const router = useRouter()

router.beforeEach((to) => {
  if (!isAuthenticated.value && to.name !== 'login') return { name: 'login' }
  if (!isAdmin.value && to.name && RestrictedRoutes.includes(to.name)) return { name: 'home' }
})
</script>

<template>
  <div class="h-full min-h-screen bg-base-200">
    <RouterView :class="['h-screen', { 'pb-16': isAuthenticated }]" />
  </div>
  <NavigationBar v-if="isAuthenticated" class="h-16" />
</template>
