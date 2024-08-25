<script setup lang="ts">
import { computed } from 'vue'
import type { AnimalInfo } from '../declarations'
import humanizeDuration from 'humanize-duration'

const props = defineProps<{
  animal: AnimalInfo
  size: 'compact' | 'regular'
}>()

const placerholderImage = '/images/dog.png'

const age = computed(() => {
  if (!props.animal.birthDate) return

  const ageMs = Math.max(
    1 * 24 * 60 * 60 * 1000, // 1 day is the smallest amount of time displayed
    new Date().valueOf() - props.animal.birthDate.valueOf()
  )
  return humanizeDuration(ageMs, {
    language: 'es',
    units: ['y', 'mo', 'd'],
    largest: 1,
    round: false,
    maxDecimalPoints: 0
  })
})
</script>

<template>
  <article class="flex items-center gap-4 rounded-2xl bg-secondary-content px-3 py-2.5 shadow-sm">
    <div class="flex w-full items-center gap-4">
      <img
        :class="[
          'rounded-full border-2 border-secondary object-cover shadow-xl',
          props.size === 'compact' ? 'h-12 w-12' : 'h-16 w-16'
        ]"
        :src="props.animal.image ?? placerholderImage"
        alt="User profile avatar image"
      />
      <section class="flex flex-grow flex-col gap-2">
        <header class="flex items-center gap-3">
          <p class="text-xl font-semibold">{{ props.animal.name }}</p>
          <span
            v-if="props.size === 'regular'"
            :class="[
              'text-2xl text-secondary',
              props.animal.sex === 'male' ? 'i-mingcute-male-line' : 'i-mingcute-female-line'
            ]"
          />
        </header>

        <div v-if="props.size === 'regular'" class="flex w-full gap-4">
          <div class="flex max-w-[40%] items-center gap-1">
            <span class="i-mingcute-location-fill flex-shrink-0 text-xl text-secondary" />
            <p class="truncate">{{ props.animal.yard?.name ?? 'Sin patio' }}</p>
          </div>

          <div class="flex items-center gap-1">
            <span class="i-mingcute-birthday-2-fill text-xl text-secondary" />
            <p>{{ age ?? 'Sin patio' }}</p>
          </div>
        </div>
      </section>

      <div v-if="$slots.action" class="self-start">
        <slot name="action" />
      </div>
    </div>
  </article>
</template>
