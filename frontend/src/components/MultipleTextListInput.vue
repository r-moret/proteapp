<script setup lang="ts" generic="T extends Record<string, string | null | undefined>">
import TextInput from './TextInput.vue'
import { ref } from 'vue'
import { isEqual } from 'lodash'

const props = defineProps<{
  modelValue?: T[] | null
  placeholder?: string
}>()

const emit = defineEmits<{
  add: [text: string]
  'update:model-value': [items: T[]]
}>()

const newText = ref<string>()

function handleRemoveItem(item: T) {
  emit(
    'update:model-value',
    props.modelValue!.filter((savedItem) => !isEqual(savedItem, item))
  )
}

function handleCreateNewItem() {
  if (!newText.value) return
  emit('add', newText.value)
  newText.value = undefined
}
</script>

<template>
  <div class="flex flex-col gap-3">
    <div class="flex gap-2">
      <TextInput
        v-model="newText"
        :placeholder="props.placeholder"
        @keydown.enter="handleCreateNewItem"
      >
        <template #icon>
          <slot name="inputIcon">
            <span class="i-mingcute-pencil-2-line text-2xl text-secondary" />
          </slot>
        </template>
      </TextInput>
      <button
        class="flex w-16 items-center justify-center rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
        @click="handleCreateNewItem"
      >
        <span class="i-mingcute-add-line text-2xl font-bold" />
      </button>
    </div>
    <ul class="h-fit max-h-56 w-full overflow-y-scroll rounded-xl bg-white px-4 py-3">
      <template v-if="props.modelValue?.length">
        <li v-for="(item, index) in props.modelValue" :key="index">
          <div class="flex items-start justify-between">
            <slot name="item" :item="item" />
            <button class="flex items-center" @click="handleRemoveItem(item)">
              <span class="i-mingcute-close-line" />
            </button>
          </div>
          <span v-if="index !== props.modelValue?.length - 1" class="divider m-0" />
        </li>
      </template>
      <template v-else>
        <slot name="empty" />
      </template>
    </ul>
  </div>
</template>
