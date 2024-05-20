<script setup lang="ts">
import AnimalDetails from '@/modules/Animal/components/AnimalDetails.vue'
import AnimalImage from '@/modules/Animal/components/AnimalImage.vue'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAnimalStore } from '@/store/AnimalStore'
import humanizeDuration from 'humanize-duration'
import { format } from '@formkit/tempo'

const { getAnimal } = useAnimalStore()

const router = useRouter()
const route = useRoute()

const navigateBack = () => router.back()

const animal = computed(() => getAnimal(route.params.id as string))
const age = computed(() => {
  if (!animal.value) return

  const ageMs = Math.max(0, new Date().valueOf() - animal.value.birthDate.valueOf())
  return humanizeDuration(ageMs, {
    language: 'es',
    units: ['y', 'mo', 'd'],
    largest: 1,
    round: false
  })
})
</script>

<template>
  <div v-if="animal" class="">
    <div class="relative h-1/2 w-screen overflow-hidden shadow-2xl">
      <div
        class="absolute left-0 top-0 mx-3 mt-4 flex items-center justify-center rounded-xl bg-black bg-opacity-40 p-1 backdrop-blur-lg"
        @click="navigateBack"
      >
        <span class="i-mingcute-left-line text-4xl text-white" />
      </div>
      <div
        :class="[
          'indicator absolute right-0 top-0 mx-3 mt-4 flex items-center justify-center rounded-xl bg-black bg-opacity-40 p-1 text-white backdrop-blur-lg'
        ]"
      >
        <span
          v-if="animal.hasTreatment"
          class="badge indicator-item badge-secondary badge-md indicator-start font-semibold"
        >
          !
        </span>
        <span class="i-mingcute-stethoscope-line text-4xl" />
      </div>
      <AnimalImage :image="animal.image" class="h-full w-full object-cover" />
      <div
        class="absolute inset-x-0 bottom-0 flex h-1/6 items-center gap-2 bg-black bg-opacity-40 px-6 backdrop-blur-lg"
      >
        <div class="flex flex-col">
          <p class="text-2xl font-semibold text-white">{{ animal.name }}</p>
          <p class="text-xs italic text-white">{{ animal.personality }}</p>
        </div>

        <p class="ml-auto text-lg font-semibold text-white">{{ age }},</p>
        <span
          :class="[
            'text-2xl text-white',
            animal.sex == 'male' ? 'i-mingcute-male-line' : 'i-mingcute-female-line'
          ]"
        />
      </div>
    </div>
    <div class="flex flex-col gap-3 px-6 pt-4">
      <AnimalDetails
        :birth-date="animal.birthDate"
        :is-castrated="animal.isCastrated"
        :is-compatible="animal.isAnimalCompatible"
        :location="animal.yard"
        class="my-3 bg-base-300"
      />
      <div class="flex items-center gap-2">
        <span class="i-mingcute-calendar-2-line text-3xl" />
        <p>Entró el {{ format(animal.entryDate, 'medium', 'es-ES') }}</p>
      </div>
      <p>{{ animal.description }}</p>
      <p>{{ animal.description }}</p>
      <p>{{ animal.description }}</p>
      <p>{{ animal.description }}</p>
      <p>{{ animal.description }}</p>
      <p>{{ animal.description }}</p>
      <p>{{ animal.description }}</p>
      <p>{{ animal.description }}</p>
    </div>
  </div>
</template>
