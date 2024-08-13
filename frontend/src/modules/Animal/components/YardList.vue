<script setup lang="ts">
import type { YardInfo } from '../declarations'
import ItemList from '@/components/ItemList.vue'
import { useAnimalStore } from '@/store/AnimalStore'
import { useToastNotifications } from '@/composable/useToastNotifications'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { ref } from 'vue'
import YardCard from '@/modules/Animal/components/YardCard.vue'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)
const animalStore = useAnimalStore()

async function handleDeleteYard(yardId: string) {
  try {
    await animalStore.deleteYard(yardId)
    showSuccessNotification('Patio eliminado correctamente')
  } catch (error) {
    showErrorNotification('Ha ocurrido un error, prueba otra vez.')
  }
}

const props = defineProps<{
  yardList: YardInfo[]
}>()
</script>

<template>
  <ToastNotifications ref="notificationsRef" />

  <div class="flex h-3/4 w-full flex-col">
    <ItemList
      :items="props.yardList"
      delete-title="¿Estás seguro de que quieres borrar este patio?"
      class="mx-5"
      @delete="(yard) => handleDeleteYard(yard.id)"
    >
      <template #empty>
        <div class="mt-6 flex flex-col items-center">
          <span class="i-mingcute-heart-crack-fill text-6xl" />
          <p class="text-gray-500">No hay patios</p>
        </div>
      </template>
      <template #item="{ item, openConfirm }">
        <YardCard :yard="item">
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
