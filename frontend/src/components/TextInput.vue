<script setup lang="ts">
const model = defineModel<string | null>()

const props = defineProps<{
  name?: string
  placeholder?: string
  type?: string
}>()
</script>

<template>
  <div class="flex h-12 w-full">
    <template v-if="$slots.icon">
      <div class="flex items-center justify-center rounded-l-lg bg-white px-3">
        <slot name="icon"></slot>
      </div>
      <div class="divider divider-horizontal mx-0 w-fit bg-white py-2" />
    </template>
    <input
      :type="props.type ?? 'text'"
      :class="['h-full w-full px-4', $slots.icon ? 'rounded-r-lg' : 'rounded-lg']"
      :placeholder="props.placeholder"
      autocomplete="off"
      v-model="model"
      v-bind="props.name ? { name: props.name, id: props.name } : null"
    />
  </div>
</template>
