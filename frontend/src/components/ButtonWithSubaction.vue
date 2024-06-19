<script setup lang="ts">
const props = defineProps<{
  showSubaction: boolean
}>()
</script>

<template>
  <div class="flex items-center gap-1">
    <div :class="['z-10 transition-all', { 'translate-x-4': !props.showSubaction }]">
      <slot name="main-button" />
    </div>
    <div
      :class="[
        'w-8 overflow-hidden transition-all duration-200',
        props.showSubaction ? 'translate-x-0' : 'invisible -translate-x-6'
      ]"
    >
      <slot name="subaction-button" />
    </div>
  </div>
</template>

<style scoped></style>
