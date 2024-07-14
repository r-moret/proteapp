<script setup lang="ts" generic="T extends { [key: string]: any }">
import { useSlots, onBeforeMount } from 'vue'

const props = withDefaults(
  defineProps<{
    items?: T[] | null
    title?: keyof T
    canDelete?: boolean
    labels?: Partial<Record<keyof T, string>>
    formatters?: Partial<Record<keyof T, (value: any) => string>>
  }>(),
  {
    canDelete: true
  }
)

const emit = defineEmits<{
  delete: [payload: T]
}>()

const slots = useSlots()

function formatField(field: keyof T, value: any) {
  if (!props.formatters?.[field]) return value

  return props.formatters[field](value)
}

onBeforeMount(() => {
  if (!slots.item && (!props.labels || !props.title)) {
    throw Error(
      'One of item slot or field labels and title props must be provided in order to render the list'
    )
  }
})
</script>

<template>
  <div class="flex-1 overflow-y-auto">
    <slot v-if="!items || !items.length" name="empty" />

    <ul v-else class="space-y-2">
      <li v-for="(item, index) in props.items" :key="index">
        <span v-if="index != 0" class="divider my-0" />
        <slot name="item" :item="item">
          <div class="flex flex-row justify-between px-4 py-2">
            <div class="flex flex-col">
              <p class="mb-1 text-lg font-semibold text-blue-600">{{ item[props.title!] }}</p>
              <template v-for="(label, field) in props.labels" :key="field">
                <p v-if="item[field]" class="text-base text-gray-700">
                  {{ label }}: {{ formatField(field, item[field]) }}
                </p>
              </template>
            </div>
            <button class="my-1 flex flex-col" @click="emit('delete', item)">
              <span class="i-mingcute-close-fill text-xl text-gray-400" />
            </button>
          </div>
        </slot>
      </li>
    </ul>
  </div>
</template>
