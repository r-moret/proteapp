<script setup lang="ts">
import ItemList from '@/components/ItemList.vue'
import AdoptionCard from '@/modules/Adoption/components/AdoptionCard.vue'
import { useAdoptionStore } from '@/store/AdoptionStore'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToastNotifications } from '@/composable/useToastNotifications'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { format } from '@formkit/tempo'
import type { AdoptionInfo } from '../declarations'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)
const adoptionStore = useAdoptionStore()
const router = useRouter()

const navigateAdoption = (id: string) => router.push({ name: 'adoption', params: { id } })

async function handleDeleteAdoption(adoptionId: string) {
  try {
    await adoptionStore.deleteAdoption(adoptionId)
    showSuccessNotification('Adopción eliminada correctamente')
  } catch (error) {
    showErrorNotification('Ha ocurrido un error, prueba otra vez.')
  }
}
const props = defineProps<{
  adoptionList: AdoptionInfo[]
}>()
</script>

<template>
  <div>
    <ToastNotifications ref="notificationsRef" />
    <ItemList
      :items="props.adoptionList"
      delete-title="¿Estás seguro de que quieres borrar esta adopción?"
      @delete="(adoption) => handleDeleteAdoption(adoption.id)"
    >
      <template #empty>
        <div class="mt-6 flex flex-col items-center">
          <span class="i-mingcute-heart-crack-fill text-6xl" />
          <p class="text-gray-500">No hay adopciones</p>
        </div>
      </template>
      <template #item="{ item, openConfirm }">
        <AdoptionCard :adoption="item" @click="navigateAdoption(item.id)">
          <template #action>
            <button class="my-1 flex flex-col" @click.stop="openConfirm(item)">
              <span class="i-mingcute-close-fill text-xl text-gray-400" /></button
          ></template>
        </AdoptionCard>
      </template>
      <template #delete="{ item }">
        <p>
          <span class="font-semibold">{{ item.animal.name }}</span>
          <span>
            {{ `, el día ${format(item.registerDate, { date: 'medium' })} ` }}
          </span>
          <span>por {{ item.person.name }} {{ item.person.firstSurname }}</span>
        </p>
      </template>
    </ItemList>
  </div>
</template>
