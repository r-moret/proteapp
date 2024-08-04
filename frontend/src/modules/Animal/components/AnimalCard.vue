<script setup lang="ts">
import type { AnimalInfo } from '../declarations'

const props = defineProps<{
  animal: AnimalInfo
  size: 'compact' | 'regular'
}>()

const placerholderImage = '/images/dog.png'
</script>

<template>
  <article
    :class="['flex items-center gap-4 rounded-2xl bg-secondary-content px-3 py-2 shadow-sm']"
  >
    <img
      :class="[
        'rounded-full border-2 border-secondary object-cover shadow-xl',
        props.size === 'compact' ? 'h-12 w-12' : 'h-16 w-16'
      ]"
      :src="props.animal.image ?? placerholderImage"
      alt="User profile avatar image"
    />
    <section>
      <header class="flex items-center gap-3">
        <p class="text-lg font-semibold">{{ props.animal.name }}</p>
        <span class="i-mingcute-male-line text-2xl text-secondary" />
      </header>
      <!-- <div v-if="props.size === 'regular'" class="italic">{{ props.user.person.email }}</div> -->
    </section>
  </article>
</template>
