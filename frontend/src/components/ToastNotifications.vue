<script setup lang="ts">
import { ref } from 'vue'
import type { Notification } from '@/types'

defineExpose({
  addNotification,
  removeNotification
})

const notifications = ref<Notification[]>([])

function addNotification(notif: Notification) {
  notifications.value.push(notif)
}

function removeNotification(id: string) {
  notifications.value = notifications.value.filter((notif) => notif.id !== id)
}
</script>

<template>
  <div v-if="notifications.length" class="toast toast-center toast-top z-50 w-full pt-6">
    <div
      v-for="notification in notifications"
      :class="[
        'alert alert-info flex items-stretch justify-start border-2 shadow-2xl',
        notification.cardStyle ?? 'border-secondary bg-white'
      ]"
      :key="notification.id"
    >
      <div v-if="notification.icon">
        <span
          :class="[
            'flex flex-none items-center text-2xl',
            notification.icon,
            notification.iconStyle ?? 'text-secondary'
          ]"
        />
      </div>
      <p :class="['text-wrap font-semibold', notification.textStyle ?? 'text-black']">
        {{ notification.text }}
      </p>
      <button class="ml-auto flex flex-none pl-2" @click="removeNotification(notification.id)">
        <span class="i-mingcute-close-fill text-gray-700" />
      </button>
    </div>
  </div>
</template>
