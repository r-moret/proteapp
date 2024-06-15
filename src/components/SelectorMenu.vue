<script setup lang="ts">
import { every } from 'lodash'
import { computed } from 'vue'

enum OPTIONS {
  ALL = 'checkAll'
}

const props = defineProps<{
  modelValue: Record<string, boolean>
  includeAllControl: boolean
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', payload: Record<string, boolean>): void
}>()

const areAllChecked = computed(() => every(props.modelValue, (value) => value))

const toggleAll = (newValue: boolean) => {
  const allCheckedValues = Object.keys(props.modelValue).reduce(
    (acc, option) => ({ ...acc, [option]: newValue }),
    {}
  )
  emit('update:modelValue', allCheckedValues)
}

const updateCheckbox = (option: string, event: Event) => {
  const newValue = (event.target as HTMLInputElement).checked

  if (option === OPTIONS.ALL) {
    toggleAll(newValue)
    return
  }
  emit('update:modelValue', { ...props.modelValue, [option]: newValue })
}
</script>

<template>
  <div class="form-control">
    <template v-if="props.includeAllControl">
      <label class="label gap-4">
        <input
          type="checkbox"
          class="checkbox-secondary checkbox"
          :checked="areAllChecked"
          @change="(event) => updateCheckbox(OPTIONS.ALL, event)"
        />
        <span class="label-text w-full text-start font-semibold capitalize">Todos</span>
      </label>
      <div class="divider my-1" />
    </template>
    <label v-for="(isChecked, option) in modelValue" :key="option" class="label gap-4">
      <input
        type="checkbox"
        class="checkbox-secondary checkbox"
        :checked="isChecked"
        @change="(event) => updateCheckbox(option, event)"
      />
      <span class="label-text w-full text-start font-semibold capitalize">{{ option }}</span>
    </label>
  </div>
</template>
