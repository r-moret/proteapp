<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  options: string[]
}>()

const checkedOptions = defineModel<string[]>('checked', { required: true })

const areAllChecked = computed(() => checkedOptions.value.length == props.options.length)

const toggleAllOption = (event: Event) => {
  const checkbox = event.target as HTMLInputElement
  const checked = checkbox.checked

  if (checked) {
    checkedOptions.value = [...props.options]
  } else {
    checkedOptions.value = []
  }
}
</script>

<template>
  <div class="form-control">
    <label class="label cursor-pointer gap-4">
      <input
        type="checkbox"
        class="checkbox-secondary checkbox"
        :checked="areAllChecked"
        @change="toggleAllOption"
      />
      <span class="label-text w-full text-start font-semibold">Todos</span>
    </label>
    <div class="divider my-1" />
    <label v-for="option in props.options" :key="option" class="label cursor-pointer gap-4">
      <input
        type="checkbox"
        v-model="checkedOptions"
        :value="option"
        class="checkbox-secondary checkbox"
      />
      <span class="label-text w-full text-start font-semibold">{{ option }}</span>
    </label>
  </div>
</template>
