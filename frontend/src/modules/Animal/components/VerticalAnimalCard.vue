<script setup lang="ts">
import type { AnimalInfo } from '@/modules/Animal/declarations'
import AnimalImage from './AnimalImage.vue'

const props = defineProps<{
  animal: AnimalInfo
}>()
</script>

<template>
  <div class="overflow-hidden">
    <figure class="grid h-40 w-32 place-content-center">
      <AnimalImage :image="animal.image" class="col-start-1 row-start-1 h-40 w-32 rounded-xl" />
      <div
        class="col-start-1 row-start-1 flex h-fit w-32 items-center justify-between self-end bg-black bg-opacity-40 px-4 py-2 backdrop-blur-sm"
      >
        <h2 class="truncate font-semibold text-white">{{ props.animal.name }}</h2>
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
