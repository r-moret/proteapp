<script setup lang="ts">
import { ref } from 'vue'

import DateInput from '@/components/DateInput.vue'

import AppHeader from '@/skeleton/AppHeader.vue'

const date = ref()
</script>

<template>
  <main class="flex flex-col items-end">
    <AppHeader title="Informe" />
    <section class="min-h-0 w-full flex-grow">
      <DateInput class="mb-4 mt-2" v-model="date" />
    </section>
  </main>
</template>
