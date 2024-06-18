import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { fakeAppointments } from '@/fakes'
import { sleep } from '@/utils'
import type { MedicalAppointment } from '@/types'

export const useAppointmentStore = defineStore('AppointmentStore', () => {
  const appointmentList = ref<MedicalAppointment[]>([])
  const isLoading = ref<boolean>(false)

  const getAppointment = computed(() => (id: string): MedicalAppointment | undefined => {
    return appointmentList.value.find((appointment) => appointment.id == id)
  })

  async function fetchAppointments() {
    isLoading.value = true
    await sleep(3000)
    appointmentList.value = fakeAppointments
    isLoading.value = false
  }

  return {
    appointmentList,
    getAppointment,
    fetchAppointments
  }
})
