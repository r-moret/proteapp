<script setup lang="ts">
import ItemList from '@/components/ItemList.vue'
import type { UserInfo } from '@/modules/User/declarations'
import UserCard from '@/modules/Inform/components/UserCard.vue'
import { useUserStore } from '@/store/UserStore'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { ref } from 'vue'
import ToastNotifications from '@/components/ToastNotifications.vue'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)

const userStore = useUserStore()
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const props = defineProps<{
  userList: UserInfo[]
}>()

const emit = defineEmits<{
  clickUser: [payload: UserInfo]
}>()

async function handleDeleteUser(userId: string) {
  try {
    await userStore.deleteUser(userId)
    showSuccessNotification('Usuario eliminado correctamente')
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
      :items="props.userList"
      delete-title="¿Estás seguro de que quieres borrar este usuario?"
      @delete="(user) => handleDeleteUser(user.id)"
    >
      <template #empty>
        <div class="mt-6 flex flex-col items-center">
          <span class="i-mingcute-heart-crack-fill text-6xl" />
          <p class="text-gray-500">No hay usuarios</p>
        </div>
      </template>
      <template #item="{ item, openConfirm }">
        <UserCard :user="item" size="regular" @click="emit('clickUser', item)">
          <template #action>
            <button class="my-1 flex flex-col" @click.stop="openConfirm(item)">
              <span class="i-mingcute-close-fill text-xl text-gray-400" /></button
          ></template>
        </UserCard>
      </template>
      <template #delete="{ item }">
        <p>
          <span class="font-semibold">{{
            getFullName(item.person.name, item.person.firstSurname, item.person.secondSurname)
          }}</span>
        </p>
      </template>
    </ItemList>
  </div>
</template>
