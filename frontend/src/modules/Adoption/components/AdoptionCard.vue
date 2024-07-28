<script setup lang="ts">
import { computed } from 'vue'
import type { AdoptionInfo } from '@/modules/Adoption/declarations'
import { format } from '@formkit/tempo'

const props = defineProps<{
  adoption: AdoptionInfo
}>()

const placeholderImage = computed(() => '/images/dog.png')
</script>

<template>
  <article
    :class="['flex items-center gap-4 rounded-2xl bg-secondary-content px-3 py-2 shadow-sm']"
  >
    <div class="flex w-full items-start gap-4">
      <img
        :class="[
          'h-[4.5rem] w-[4.5rem] rounded-full border-2 border-secondary object-cover shadow-xl'
        ]"
        :src="props.adoption.animal.image ?? placeholderImage"
        alt="Adoption animal avatar image"
      />
      <section class="flex flex-grow flex-col gap-2">
        <header>
          <div class="flex flex-col gap-0.5">
            <p class="text-xl font-semibold">{{ props.adoption.animal.name }}</p>
            <p class="italic">
              Adoptado el {{ format(props.adoption.registerDate, { date: 'medium' }) }}
            </p>
          </div>
        </header>
        <div class="flex flex-col">
          <div class="flex items-center gap-1">
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
