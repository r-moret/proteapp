<script setup lang="ts">
import ItemList from '@/components/ItemList.vue'
import YardCard from '@/modules/Yard/components/YardCard.vue'

import type { YardInfo } from '@/modules/Yard/declarations'

const model = defineModel<YardInfo[]>()

const props = defineProps<{
  editMode: boolean
}>()

const emit = defineEmits<{
  delete: [payload: YardInfo]
}>()

function handleMoveYard(yard: YardInfo, direction: 'up' | 'down') {
  const yardIndex = model.value?.findIndex((savedYard) => savedYard.id === yard.id)

  if (yardIndex == undefined || !model.value) return

  if (direction === 'up') {
    ;[model.value[yardIndex], model.value[yardIndex - 1]] = [
      model.value[yardIndex - 1],
      model.value[yardIndex]
    ]
  } else {
    ;[model.value[yardIndex], model.value[yardIndex + 1]] = [
      model.value[yardIndex + 1],
      model.value[yardIndex]
    ]
  }
}
</script>

<template>
  <div class="flex h-3/4 w-full flex-col">
    <ItemList
      :items="model"
      delete-title="¿Estás seguro de que quieres borrar este patio?"
      class="mx-5"
      @delete="(yard) => emit('delete', yard)"
    >
      <template #empty>
        <div class="mt-6 flex flex-col items-center">
          <span class="i-mingcute-heart-crack-fill text-6xl" />
          <p class="text-gray-500">No hay patios</p>
        </div>
      </template>
      <template #item="{ item, index, openConfirm }">
        <YardCard
          :yard="item"
          :arrow-up="props.editMode && index !== 0"
          :arrow-down="props.editMode && index !== model!.length - 1"
          @move-up="handleMoveYard(item, 'up')"
          @move-down="handleMoveYard(item, 'down')"
        >
          <template #action>
            <button class="my-1 flex flex-col" @click.stop="openConfirm(item)">
              <span class="i-mingcute-close-fill text-xl text-gray-400" /></button
          ></template>
        </YardCard>
      </template>
      <template #delete="{ item }">
        <p>
          <span class="font-semibold">{{ item.name }}</span>
        </p>
      </template>
    </ItemList>
  </div>
</template>
