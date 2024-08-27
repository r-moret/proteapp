<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps<{
  image?: string | null
}>()

const PLACEHOLDER_IMAGE = '/images/dog.png'

const error = ref(false)
const showPlaceholder = computed(() => error.value || !props.image)

watch(
  () => props.image,
  () => {
    error.value = false
  }
)
</script>

<template>
  <img
    v-if="!showPlaceholder"
    :src="props.image!"
    alt="Image of the animal"
    @error="error = true"
    class="object-cover"
  />
  <img
    v-else
    :src="PLACEHOLDER_IMAGE"
    alt="Image of the animal"
    class="bg-base-300 object-scale-down"
  />
</template>
