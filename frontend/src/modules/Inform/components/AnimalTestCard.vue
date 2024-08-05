<script setup lang="ts">
import type { AnimalInfo } from '@/modules/Animal/declarations'

const props = defineProps<{
  animalTest: { animal: AnimalInfo; compatible: boolean }
}>()

const placeholderImage = '/images/dog.png'
</script>

<template>
  <article
    :class="['flex items-center gap-4 rounded-2xl bg-secondary-content px-3 py-2.5 shadow-sm']"
  >
    <div class="flex w-full items-center gap-4">
      <img
        :class="['h-12 w-12 rounded-full border-2 border-secondary object-cover shadow-xl']"
        :src="props.animalTest.animal.image ?? placeholderImage"
        alt="Tested animal avatar image"
      />
      <section class="flex flex-grow flex-col gap-1">
        <header class="flex items-center gap-3">
          <p class="text-xl font-semibold">{{ props.animalTest.animal.name }}</p>
          <div
            :class="[
              'badge font-semibold uppercase',
              props.animalTest.compatible ? 'badge-secondary' : 'border-secondary'
            ]"
          >
            {{ props.animalTest.compatible ? 'COMPATIBLE' : 'NO COMPATIBLE' }}
          </div>
        </header>
      </section>
      <div class="self-start">
        <slot name="action" />
      </div>
    </div>
  </article>
</template>
