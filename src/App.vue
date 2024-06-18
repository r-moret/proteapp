<script setup lang="ts">
import NavigationBar from '@/skeleton/NavigationBar.vue'
import { onBeforeMount } from 'vue'
import { RouterView } from 'vue-router'
import { useAnimalStore } from './store/AnimalStore'
import { useUserStore } from './store/UserStore'
import { useTreatmentStore } from './store/TreatmentStore'
import { useAppointmentStore } from './store/AppointmentStore'

const animalStore = useAnimalStore()
const userStore = useUserStore()
const treatmentStore = useTreatmentStore()
const appointmentStore = useAppointmentStore()

onBeforeMount(async () => {
  Promise.allSettled([
    animalStore.fetchAnimals(),
    userStore.fetchUser(),
    treatmentStore.fetchTreatments(),
    appointmentStore.fetchAppointments()
  ])
})
</script>

<template>
  <RouterView class="h-screen bg-base-200 pb-16" />
  <NavigationBar class="h-16" />
</template>
