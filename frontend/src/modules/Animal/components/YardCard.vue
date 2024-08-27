<script setup lang="ts">
import type { YardInfo } from '../declarations'

const props = defineProps<{
  yard: YardInfo
}>()
</script>

<template>
  <article class="flex items-center gap-2 rounded-xl bg-secondary-content px-3 py-2.5 shadow-sm">
    <span class="i-mingcute-location-line text-2xl text-secondary" />
    <p class="font-semibold">{{ props.yard.name }}</p>
  </article>
</template>
