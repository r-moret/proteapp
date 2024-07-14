import ToastNotifications from '@/components/ToastNotifications.vue'
import type { Notification } from '@/types'
import { uniqueId } from 'lodash'
import type { Ref } from 'vue'

export function useToastNotifications(
  reference: Ref<InstanceType<typeof ToastNotifications> | null>
) {
  function showErrorNotification(text: string, time?: number) {
    addNotification(
      {
        icon: 'i-mingcute-close-circle-line',
        text,
        cardStyle: 'border-error bg-white',
        iconStyle: 'text-error'
      },
      time
    )
  }

  function showInfoNotification(text: string, time?: number) {
    addNotification({ icon: 'i-mingcute-information-line', text }, time)
  }

  function showSuccessNotification(text: string, time?: number) {
    addNotification(
      {
        icon: 'i-mingcute-check-fill',
        text,
        cardStyle: 'border-success bg-white',
        iconStyle: 'text-success'
      },
      time
    )
  }

  function addNotification(notif: Omit<Notification, 'id'>, time: number = 15) {
    if (!reference.value)
      throw Error('A valid ToastNotification reference is needed to add notifications')

    const newId = uniqueId('notif')
    reference.value.addNotification({ ...notif, id: newId })

    setTimeout(() => {
      if (!reference.value) return
      reference.value.removeNotification(newId)
    }, 1000 * time)
  }

  return {
    showInfoNotification,
    showErrorNotification,
    showSuccessNotification,
    addNotification
  }
}
