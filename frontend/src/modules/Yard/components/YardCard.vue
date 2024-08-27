<script setup lang="ts">
import type { YardInfo } from '@/modules/Yard/declarations'

const props = defineProps<{
  yard: YardInfo
}>()
</script>

<template>
  <article
    :class="['flex items-center gap-4 rounded-2xl bg-secondary-content px-3 py-2 shadow-sm']"
  >
    <div class="flex w-full items-start gap-4">
      <section class="flex flex-grow flex-col gap-2">
        <header>
          <div class="flex flex-col gap-0.5">
            <p class="text-xl font-semibold">{{ props.yard.name }}</p>
          </div>
        </header>
      </section>
      <div class="self-start">
        <slot name="action" />
      </div>
    </div>
  </article>
</template>
