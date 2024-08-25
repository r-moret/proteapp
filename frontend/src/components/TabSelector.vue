<script setup lang="ts">
type Tabs = string[]
type Tab = Tabs[number]

const model = defineModel<Tab>()

const props = defineProps<{
  tabs: Tabs
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
