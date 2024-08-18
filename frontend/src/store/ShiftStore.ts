import { computed } from 'vue'
import { defineStore } from 'pinia'
import { useWebSocket } from '@vueuse/core'
import { ShiftStatusAdapter } from '@/modules/Shift/adapters'

export const useShiftStore = defineStore('ShiftStore', () => {
  const {
    data: statusData,
    status: statusConnection,
    close: statusClose,
    open: statusOpen
  } = useWebSocket<string>(`${import.meta.env.VITE_BACKEND_URL}/shift/status`, {
    immediate: false
  })

  const isConnecting = computed(() => statusConnection.value === 'CONNECTING')

  const status = computed(() => {
    if (!statusData.value) return undefined
    return ShiftStatusAdapter(JSON.parse(statusData.value)).status
  })

  function startConnection() {
    statusOpen()
  }

  function finishConnection() {
    statusClose()
  }

  return {
    status,
    isConnecting,

    startConnection,
    finishConnection
  }
})
