<script setup lang="ts">
import AnimalImage from '@/modules/Animal/components/AnimalImage.vue'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import humanizeDuration from 'humanize-duration'
import type { Animal } from '@/types.ts'

const props = defineProps<{
  animal: Animal
}>()

const castration = computed(() => (props.animal.isCastrated ? 'Castrado' : 'Sin castrar'))
const animalCompatibility = computed(() => {
  return props.animal.isAnimalCompatible ? 'Compatible' : 'No compatible'
})
const age = computed(() => {
  const ageMs = Math.max(0, new Date().valueOf() - props.animal.birthDate.valueOf())
  return humanizeDuration(ageMs, {
    language: 'es',
    units: ['y', 'mo', 'd'],
    largest: 1,
    round: false
  })
})

const router = useRouter()

const openAnimalView = () => {
  router.push({
    name: 'animal',
    params: { id: props.animal.id }
  })
}
</script>

<template>
  <div class="card card-side mx-0 my-0 h-32 gap-6 rounded-none" @click="openAnimalView">
    <div class="indicator my-auto h-fit w-fit">
      <div
        v-if="props.animal.hasTreatment"
        class="indicator-item indicator-start flex h-14 w-14 items-end justify-end"
      >
        <span class="flex h-fit w-fit items-center rounded-full bg-secondary p-0.5">
          <span class="i-mingcute-stethoscope-line text-3xl text-secondary-content" />
        </span>
      </div>
      <figure class="flex-shrink-0 rounded-2xl">
        <AnimalImage :image="props.animal.image" class="h-28 w-28 object-cover" />
      </figure>
    </div>
    <div class="card-body gap-2 overflow-hidden px-0 py-3">
      <div class="flex items-center gap-3">
        <h2 class="card-title mr-auto text-xl font-bold">{{ props.animal.name }}</h2>
        <span
          :class="[
            'text-xl',
            props.animal.sex == 'male'
              ? 'i-mingcute-male-line text-secondary'
              : 'i-mingcute-female-line text-accent'
          ]"
        />
      </div>
      <div>
        <p class="text-sm font-semibold">{{ age }}</p>
        <div class="flex items-center gap-2">
          <p class="flex-none text-sm text-neutral-500">{{ castration }}</p>
          –
          <p class="flex-none text-sm text-neutral-500">{{ animalCompatibility }}</p>
        </div>
        <p class="truncate text-sm text-neutral-500">{{ props.animal.personality }}</p>
      </div>
    </div>
  </div>
</template>
