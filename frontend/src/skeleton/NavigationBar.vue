<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { navigationBarConfig } from '@/config/NavigationBar'

const route = useRoute()
</script>

<template>
  <div class="btm-nav">
    <RouterLink
      v-for="view in navigationBarConfig.items"
      :to="{ name: view.name }"
      :class="['transition-colors', { 'text-secondary': view.name == route.name }]"
      :key="view.name"
    >
      <span :class="['text-2xl', view.name == route.name ? view.activeIcon : view.icon]" />
      <p class="text-xs font-semibold">{{ view.label }}</p>
    </RouterLink>
  </div>
</template>
