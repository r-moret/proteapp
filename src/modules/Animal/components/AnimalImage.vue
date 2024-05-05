<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  image?: string
}>()

const PLACEHOLDER_IMAGE = '/images/dog.png'

const validSource = ref<string>(props.image || PLACEHOLDER_IMAGE)

const setPlaceholder = () => (validSource.value = PLACEHOLDER_IMAGE)
</script>

<template>
  <img
    :src="validSource"
    alt="Image of the animal"
    @error="setPlaceholder"
    :class="{ 'bg-base-300 p-3': validSource == PLACEHOLDER_IMAGE }"
  />
</template>
