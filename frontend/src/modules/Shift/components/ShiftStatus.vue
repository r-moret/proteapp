<script setup lang="ts">
const props = defineProps<{
  status: 'open' | 'closed'
}>()
</script>

<template>
  <span
    :class="[
      'badge rounded-md px-3 py-3',
      props.status === 'open' ? 'bg-secondary bg-opacity-20' : 'bg-neutral bg-opacity-20'
    ]"
  >
    <div v-if="props.status === 'open'" class="mr-2 grid grid-cols-1 grid-rows-1">
      <span
        class="i-mingcute-round-fill col-start-1 row-start-1 animate-[ping_1200ms_ease-out_infinite] text-xs text-secondary !delay-1000"
      />
      <span class="i-mingcute-round-fill col-start-1 row-start-1 text-xs text-secondary" />
    </div>
    <div v-else class="mr-2 flex items-center">
      <span class="i-mingcute-stop-fill text-xs text-neutral text-opacity-80" />
    </div>
    <p :class="['font-semibold', props.status === 'open' ? 'text-secondary' : 'text-neutral']">
      {{ props.status === 'open' ? 'ABIERTO' : 'CERRADO' }}
    </p>
  </span>
</template>
