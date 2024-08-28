<script setup lang="ts" generic="T extends ObjectWithId">
import { useSlots, onBeforeMount, ref } from 'vue'
import BottomDrawer from './BottomDrawer.vue'
import type { ObjectWithId } from '@/types'

const props = withDefaults(
  defineProps<{
    items?: T[] | null
    title?: keyof T
    deleteTitle?: string
    labels?: Partial<Record<keyof T, string>>
    formatters?: Partial<Record<keyof T, (value: any) => string>>
  }>(),
  {}
)

const emit = defineEmits<{
  delete: [payload: T]
}>()

const slots = useSlots()

const pendingDeleteItem = ref<T>()
const deleteConfirmationOpen = ref(false)

function formatField(field: keyof T, value: any) {
  if (!props.formatters?.[field]) return value

  return props.formatters[field](value)
}

function handleDeleteItem(close: () => void) {
  if (!pendingDeleteItem.value) return

  emit('delete', pendingDeleteItem.value)
  close()
}

function handleConfirmDeleteItem(item: T) {
  pendingDeleteItem.value = item
  deleteConfirmationOpen.value = true
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
    <slot v-if="!props.items || !props.items.length" name="empty" />
    <ul v-else>
      <li v-for="(item, index) in props.items" :key="item.id">
        <span v-if="index != 0" class="divider my-2" />
        <slot name="item" :item="item" :index="index" :open-confirm="handleConfirmDeleteItem">
          <div class="flex flex-row justify-between px-4 py-2">
            <div class="flex flex-col">
              <p class="mb-1 text-lg font-semibold text-blue-600">{{ item[props.title!] }}</p>
              <template v-for="(label, field) in props.labels" :key="field">
                <p v-if="item[field]" class="text-base text-gray-700">
                  {{ label }}: {{ formatField(field, item[field]) }}
                </p>
              </template>
            </div>
            <button class="my-1 flex flex-col" @click="handleConfirmDeleteItem(item)">
              <span class="i-mingcute-close-fill text-xl text-gray-400" />
            </button>
          </div>
        </slot>
      </li>
    </ul>

    <BottomDrawer
      v-if="pendingDeleteItem"
      class="bg-base-200"
      size="tiny"
      v-model="deleteConfirmationOpen"
      v-slot="{ close }"
    >
      <div class="flex h-full flex-col gap-6 pb-8">
        <h1 class="text-3xl font-semibold">{{ props.deleteTitle }}</h1>
        <div>
          <slot name="delete" :item="pendingDeleteItem">
            <p>
              <span v-if="props.title" class="font-semibold">
                {{ pendingDeleteItem[props.title] }}
              </span>
            </p>
          </slot>
        </div>
        <div class="mt-auto flex flex-col gap-2">
          <div class="divider my-1" />
          <div class="flex justify-center gap-10">
            <button class="rounded-lg bg-base-100 px-6 py-2 text-lg font-semibold" @click="close">
              Cancelar
            </button>
            <button
              class="rounded-lg bg-red-700 px-6 py-2 text-lg font-semibold text-white"
              @click="handleDeleteItem(close)"
            >
              Si, borrar
            </button>
          </div>
        </div>
      </div>
    </BottomDrawer>
  </div>
</template>
