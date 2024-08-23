<script setup lang="ts">
import { useFileDialog } from '@vueuse/core'
import { UseObjectUrl } from '@vueuse/components'
import AnimalImage from '@/modules/Animal/components/AnimalImage.vue'
import { computed, watchEffect } from 'vue'

const props = defineProps<{
  modelValue?: File | null
}>()

const { files, open, reset } = useFileDialog({
  accept: 'image/*',
  directory: false,
  multiple: false
})

const selectedImage = computed(() => files.value?.item(0) ?? props.modelValue ?? undefined)

const emit = defineEmits<{
  'update:modelValue': [payload: File | undefined]
}>()

function resetImage() {
  reset()
  emit('update:modelValue', undefined)
}

watchEffect(() => {
  emit('update:modelValue', selectedImage.value)
})
</script>

<template>
  <div class="flex w-full items-start">
    <div class="w-1/3">
      <div class="aspect-square flex-shrink-0">
        <AnimalImage v-if="!selectedImage" class="h-full w-full rounded-xl object-cover" />
        <UseObjectUrl v-else v-slot="url" :object="selectedImage">
          <AnimalImage class="h-full w-full rounded-xl object-cover" :image="url" />
        </UseObjectUrl>
      </div>
    </div>

    <div class="flex w-2/3 flex-col items-center gap-2 overflow-hidden py-2">
      <p class="h-6 w-full truncate px-5 text-center text-sm italic">
        {{ selectedImage?.name ?? 'Sin imagen seleccionada' }}
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
          selectedImage
            ? 'border-neutral border-opacity-30 bg-neutral bg-opacity-10 text-neutral'
            : 'border-neutral border-opacity-15 bg-neutral bg-opacity-5 text-neutral text-opacity-45'
        ]"
        @click="resetImage"
      >
        Eliminar
      </button>
    </div>
  </div>
</template>
