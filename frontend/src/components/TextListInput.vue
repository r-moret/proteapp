<script setup lang="ts">
import TextInput from './TextInput.vue'
import { ref } from 'vue'
import { uniqueId } from 'lodash'

const model = defineModel<string[] | null>()

const props = defineProps<{
  placeholder?: string
}>()

const newText = ref<string>()
const identifiedTexts = ref(model.value?.map((text) => ({ text, id: uniqueId() })))

function handleAddText() {
  if (!newText.value) return

  identifiedTexts.value?.push({ text: newText.value, id: uniqueId() })
  model.value = [...(model.value ?? []), newText.value]
  newText.value = undefined
}

function handleRemoveText(id: string) {
  identifiedTexts.value = identifiedTexts.value?.filter((idText) => idText.id !== id)
  model.value = identifiedTexts.value?.map((idText) => idText.text)
}
</script>

<template>
  <div class="flex flex-col gap-3">
    <div class="flex gap-2">
      <TextInput
        v-model="newText"
        name="inform-new-highlight"
        :placeholder="props.placeholder"
        @keydown.enter="handleAddText"
      >
        <template #icon>
          <span class="i-mingcute-pencil-2-line text-2xl text-secondary" />
        </template>
      </TextInput>
      <button
        class="flex w-16 items-center justify-center rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
        @click="handleAddText"
      >
        <span class="i-mingcute-add-line text-2xl font-bold" />
      </button>
    </div>
    <ul class="h-fit max-h-40 w-full overflow-y-scroll rounded-xl bg-white px-4 py-3">
      <template v-if="identifiedTexts?.length">
        <li v-for="(idText, index) in identifiedTexts" :key="index">
          <div class="flex h-8 items-center justify-between">
            <p>{{ idText.text }}</p>
            <button class="flex items-center" @click="handleRemoveText(idText.id)">
              <span class="i-mingcute-close-line" />
            </button>
          </div>
          <span v-if="index !== identifiedTexts?.length - 1" class="divider m-0" />
        </li>
      </template>
      <template v-else>
        <slot name="empty" />
      </template>
    </ul>
  </div>
</template>
