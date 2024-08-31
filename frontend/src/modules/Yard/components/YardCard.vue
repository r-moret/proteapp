<script setup lang="ts">
import type { YardInfo } from '@/modules/Yard/declarations'

const props = withDefaults(
  defineProps<{
    yard: YardInfo
    arrowUp?: boolean
    arrowDown?: boolean
  }>(),
  {
    arrowDown: false,
    arrowUp: false
  }
)

const emit = defineEmits<{
  moveUp: []
  moveDown: []
}>()
</script>

<template>
  <article class="flex items-center gap-4 rounded-xl bg-secondary-content px-3 py-2.5 shadow-sm">
    <section class="flex flex-grow items-center gap-2 overflow-hidden">
      <span class="i-mingcute-location-line flex-shrink-0 text-2xl text-secondary" />
      <p class="truncate text-lg font-semibold">{{ props.yard.name }}</p>
    </section>
    <div v-if="props.arrowUp || props.arrowDown" class="flex items-center gap-1">
      <button class="flex items-center" @click="emit('moveDown')" :disabled="!props.arrowDown">
        <span
          :class="[
            'i-mingcute-arrows-down-fill flex-shrink-0 text-2xl',
            { invisible: !props.arrowDown }
          ]"
        />
      </button>
      <button class="flex items-center" @click="emit('moveUp')" :disabled="!props.arrowUp">
        <span
          :class="[
            'i-mingcute-arrows-up-fill flex-shrink-0 text-2xl',
            { invisible: !props.arrowUp }
          ]"
        />
      </button>
    </div>
    <div v-if="$slots.action">
      <slot name="action" />
    </div>
  </article>
</template>
