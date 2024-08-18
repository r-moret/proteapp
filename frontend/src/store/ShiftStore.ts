import { computed } from 'vue'
import { defineStore } from 'pinia'
import { useWebSocket } from '@vueuse/core'
import { ShiftStatusAdapter, ShiftAdapter, ShiftActionAdapter } from '@/modules/Shift/adapters'
import type { ShiftAction, ShiftSelection } from '@/modules/Shift/declarations'

export const useShiftStore = defineStore('ShiftStore', () => {
  const {
    data: statusData,
    status: statusConnection,
    close: statusClose,
    open: statusOpen
  } = useWebSocket<string>(`${import.meta.env.VITE_BACKEND_URL}/shift/status`, {
    immediate: false
  })

  const {
    data: shiftData,
    status: shiftConnection,
    close: shiftClose,
    open: shiftOpen,
    send: shiftSend
  } = useWebSocket<string>(`${import.meta.env.VITE_BACKEND_URL}/shift`, {
    immediate: false
  })

  const isConnecting = computed(
    () => statusConnection.value === 'CONNECTING' || shiftConnection.value === 'CONNECTING'
  )

  const status = computed(() => {
    if (!statusData.value) return undefined
    return ShiftStatusAdapter(JSON.parse(statusData.value)).status
  })

  const shift = computed(() => {
    if (!shiftData.value) return undefined
    return ShiftAdapter(JSON.parse(shiftData.value)).timetable
  })

  const connections = computed(() => {
    if (!shiftData.value) return undefined
    return ShiftAdapter(JSON.parse(shiftData.value)).connected
  })

  function startConnection() {
    statusOpen()
    shiftOpen()
  }

  function finishConnection() {
    statusClose()
    shiftClose()
  }

  function sendShiftAction(type: ShiftAction['type'], user: string, shift: ShiftSelection) {
    const action = ShiftActionAdapter({ type, user, shift })
    shiftSend(JSON.stringify(action))
  }

  return {
    status,
    shift,
    connections,
    isConnecting,

    sendShiftAction,
    startConnection,
    finishConnection
  }
})
