import { computed } from 'vue'
import { defineStore, storeToRefs } from 'pinia'
import { useWebSocket } from '@vueuse/core'
import { useAuthStore } from '@/store/AuthStore'
import { ShiftStatusAdapter, ShiftAdapter, ShiftActionAdapter } from '@/modules/Shift/adapters'
import type { ShiftAction, ShiftSelection } from '@/modules/Shift/declarations'
import {
  wsShift as wsShiftApi,
  crudStatus as crudStatusApi,
  wsStatus as wsStatusApi,
  cleanShift as cleanShiftApi
} from '@/modules/Shift/api'
import { authFetch } from '@/composable/useAuthFetch'

const { token } = storeToRefs(useAuthStore())

export const useShiftStore = defineStore('ShiftStore', () => {
  const {
    data: statusData,
    status: statusConnection,
    close: statusClose,
    open: statusOpen
  } = useWebSocket<string>(
    `${import.meta.env.VITE_BACKEND_URL}/${wsStatusApi}?token=${token.value}`,
    {
      immediate: false
    }
  )

  const {
    data: shiftData,
    status: shiftConnection,
    close: shiftClose,
    open: shiftOpen,
    send: shiftSend
  } = useWebSocket<string>(
    `${import.meta.env.VITE_BACKEND_URL}/${wsShiftApi}?token=${token.value}`,
    {
      immediate: false
    }
  )

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

  async function toggleStatus() {
    const toggledStatus = status.value === 'open' ? 'closed' : 'open'

    const response = await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${crudStatusApi}`, {
      method: 'post',
      body: JSON.stringify({ status: toggledStatus }),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) throw Error(`Error backend response: ${await response.json()}`)
  }

  async function cleanShift() {
    const response = await authFetch(`${import.meta.env.VITE_BACKEND_URL}/${cleanShiftApi}`, {
      method: 'post'
    })

    if (!response.ok) throw Error(`Error backend response: ${await response.json()}`)
  }

  return {
    status,
    shift,
    connections,
    isConnecting,

    sendShiftAction,
    startConnection,
    finishConnection,
    toggleStatus,
    cleanShift
  }
})
