<script setup lang="ts">
import { computed } from 'vue'
import type { AdoptionInfo } from '@/modules/Adoption/declarations'
import { format } from '@formkit/tempo'
import type { Optional } from '@/types'

const props = withDefaults(
  defineProps<{
    adoption: Optional<AdoptionInfo, 'id' | 'registerDate' | 'person'>
    size?: 'compact' | 'regular'
  }>(),
  {
    size: 'regular'
  }
)

const placeholderImage = computed(() => '/images/dog.png')
</script>

<template>
  <article
    :class="['flex items-center gap-4 rounded-2xl bg-secondary-content px-3 py-2.5 shadow-sm']"
  >
    <div class="flex w-full items-center gap-4">
      <img
        :class="[
          'rounded-full border-2 border-secondary object-cover shadow-xl',
          props.size === 'compact' ? 'h-12 w-12' : 'h-[4.5rem] w-[4.5rem]'
        ]"
        :src="props.adoption.animal.image ?? placeholderImage"
        alt="Adoption animal avatar image"
      />
      <section class="flex flex-grow flex-col gap-1">
        <header class="flex items-center gap-3">
          <p class="text-xl font-semibold">{{ props.adoption.animal.name }}</p>
          <div v-if="props.adoption.foster" class="badge badge-secondary font-semibold uppercase">
            ACOGIDA
          </div>
        </header>
        <div class="flex flex-col gap-1">
          <p v-if="props.adoption.registerDate" class="italic">
            Adoptado el {{ format(props.adoption.registerDate, { date: 'medium' }) }}
          </p>
          <div v-if="props.adoption.person" class="flex items-center gap-1">
            <span class="i-mingcute-user-2-fill text-xl text-secondary" />
            <p>{{ props.adoption.person.name }} {{ props.adoption.person.firstSurname }}</p>
          </div>
        </div>
      </section>
      <div class="self-start">
        <slot name="action" />
      </div>
    </div>
  </article>
</template>
