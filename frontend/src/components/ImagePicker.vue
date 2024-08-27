<script setup lang="ts">
import { useFileDialog } from '@vueuse/core'
import AnimalImage from '@/modules/Animal/components/AnimalImage.vue'
import { computed, watch } from 'vue'
import { useObjectUrl } from '@vueuse/core'

const props = defineProps<{
  modelValue?: string | null
}>()

const { files, open, reset } = useFileDialog({
  accept: 'image/*',
  directory: false,
  multiple: false
})

const selectedImageFile = computed(() => files.value?.item(0) ?? undefined)

const emit = defineEmits<{
  'update:modelValue': [payload: string | undefined]
}>()

function resetImage() {
  reset()
  emit('update:modelValue', undefined)
}

watch(selectedImageFile, () => {
  const imageFileUrl = useObjectUrl(selectedImageFile.value)
  emit('update:modelValue', imageFileUrl.value)
})
</script>

<template>
  <div class="flex w-full items-center">
    <div class="w-1/3">
      <div class="aspect-square flex-shrink-0">
        <AnimalImage
          :image="props.modelValue"
          class="h-full w-full rounded-xl object-cover shadow-xl"
        />
      </div>
    </div>

    <div class="flex w-2/3 flex-col items-center gap-2 overflow-hidden py-2">
      <p class="h-6 w-full truncate px-5 text-center text-sm italic">
        {{ selectedImageFile?.name ?? 'Sin imagen seleccionada' }}
      </p>
      <button
        class="h-fit rounded-lg bg-secondary px-4 py-2 font-semibold text-secondary-content"
        @click="open()"
      >
        Seleccionar imagen
      </button>
      <button
        :class="[
          'h-fit w-fit rounded-lg  border px-4 py-2 font-semibold',
          props.modelValue
            ? 'border-neutral border-opacity-30 bg-neutral bg-opacity-10 text-neutral'
            : 'border-neutral border-opacity-15 bg-neutral bg-opacity-5 text-neutral text-opacity-45'
        ]"
        :disabled="!props.modelValue"
        @click="resetImage"
      >
        Eliminar
      </button>
    </div>
  </div>
</template>
