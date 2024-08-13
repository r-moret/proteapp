<script setup lang="ts">
import type { YardInfo } from '@/modules/Animal/declarations'

const props = defineProps<{
  yard: YardInfo
}>()
</script>

<template>
  <article
    :class="['flex items-center gap-4 rounded-2xl bg-secondary-content px-3 py-2 shadow-sm']"
  >
    <div class="flex w-full items-start gap-4">
      <!-- <img
        :class="[
          'h-[4.5rem] w-[4.5rem] rounded-full border-2 border-secondary object-cover shadow-xl'
        ]"
        :src="props.adoption.animal.image ?? placeholderImage"
        alt="Adoption animal avatar image"
      /> -->
      <section class="flex flex-grow flex-col gap-2">
        <header>
          <div class="flex flex-col gap-0.5">
            <p class="text-xl font-semibold">{{ props.yard.name }}</p>
          </div>
        </header>
      </section>
      <div class="self-start">
        <slot name="action" />
      </div>
    </div>
  </article>
</template>
