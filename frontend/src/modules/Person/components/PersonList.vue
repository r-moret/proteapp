<script setup lang="ts">
import ItemList from '@/components/ItemList.vue'
import type { Person } from '../declarations'
import PersonCard from './PersonCard.vue'
import { usePersonStore } from '@/store/PersonStore'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { ref } from 'vue'
import ToastNotifications from '@/components/ToastNotifications.vue'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)

const personStore = usePersonStore()
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const props = defineProps<{
  personList: Person[]
}>()

const emit = defineEmits<{
  clickPerson: [payload: Person]
}>()

async function handleDeletePerson(personId: string) {
  try {
    await personStore.deletePerson(personId)
    showSuccessNotification('Persona eliminada correctamente')
  } catch (error) {
    showErrorNotification('Ha ocurrido un error, prueba otra vez.')
  }
}

function getFullName(name: String, firstSurname: String, secondSurname: String | null | undefined) {
  return `${name} ${firstSurname}${secondSurname ? ' ' + secondSurname : ''}`
}
</script>

<template>
  <div class="flex w-full flex-col">
    <ToastNotifications ref="notificationsRef" />
    <ItemList
      :items="props.personList"
      delete-title="¿Estás seguro de que quieres borrar esta persona?"
      @delete="(person) => handleDeletePerson(person.id)"
    >
      <template #empty>
        <div class="mt-6 flex flex-col items-center">
          <span class="i-mingcute-heart-crack-fill text-6xl" />
          <p class="text-gray-500">No hay personas</p>
        </div>
      </template>
      <template #item="{ item, openConfirm }">
        <PersonCard :person="item" @click="emit('clickPerson', item)">
          <template #action>
            <button class="my-1 flex flex-col" @click.stop="openConfirm(item)">
              <span class="i-mingcute-close-fill text-xl text-gray-400" /></button
          ></template>
        </PersonCard>
      </template>
      <template #delete="{ item }">
        <p>
          <span class="font-semibold">{{
            getFullName(item.name, item.firstSurname, item.secondSurname)
          }}</span>
        </p>
      </template>
    </ItemList>
  </div>
</template>
