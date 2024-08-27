<script setup lang="ts" generic="T extends string">
const model = defineModel<T>()

const props = defineProps<{
  tabs: T[]
}>()
</script>

<template>
  <div>
    <div role="tablist" class="tabs-boxed tabs">
      <a
        v-for="tab in props.tabs"
        role="tab"
        :class="['tab font-semibold', { 'bg-secondary text-secondary-content': model === tab }]"
        :key="tab"
        @click="model = tab"
      >
        {{ tab }}
      </a>
    </div>
    <span class="divider my-0" />
  </div>
</template>
