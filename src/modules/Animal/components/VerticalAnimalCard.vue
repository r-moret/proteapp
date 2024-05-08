<script setup lang="ts">
import type { Animal } from '@/types'
import AnimalImage from './AnimalImage.vue'

const props = defineProps<{
  animal: Animal
}>()
</script>

<template>
  <div class="overflow-hidden">
    <figure class="grid h-fit w-fit place-content-center">
      <AnimalImage :image="animal.image" class="col-start-1 row-start-1 h-40 w-32 rounded-xl" />
      <div
        class="col-start-1 row-start-1 flex h-fit w-full items-center justify-between self-end bg-black bg-opacity-40 px-4 py-2 backdrop-blur-sm"
      >
        <h2 class="font-semibold text-white">{{ props.animal.name }}</h2>
        <span
          :class="[
            'text-xl text-white',
            props.animal.sex == 'male' ? 'i-mingcute-male-line' : 'i-mingcute-female-line'
          ]"
        />
      </div>
    </figure>
  </div>
</template>
