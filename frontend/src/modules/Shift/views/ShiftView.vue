<script setup lang="ts">
import { onBeforeMount, ref, computed, onBeforeUnmount } from 'vue'
import { storeToRefs } from 'pinia'

import { useUserStore } from '@/store/UserStore'
import { useAuthStore } from '@/store/AuthStore'
import { useShiftStore } from '@/store/ShiftStore'
import { useToastNotifications } from '@/composable/useToastNotifications'

import AppHeader from '@/skeleton/AppHeader.vue'
import ShiftPicker from '@/modules/Shift/components/ShiftPicker.vue'
import ShiftStatus from '@/modules/Shift/components/ShiftStatus.vue'
import ToastNotifications from '@/components/ToastNotifications.vue'

import type { EnrichedShift, ShiftSelection } from '@/modules/Shift/declarations'

const userStore = useUserStore()
const { userList } = storeToRefs(userStore)

const { loggedUser } = storeToRefs(useAuthStore())

const shiftStore = useShiftStore()
const { status, shift, connections, isConnecting } = storeToRefs(shiftStore)

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const isLoading = ref(false)

const enrichedShift = computed<EnrichedShift | undefined>(() =>
  !shift.value
    ? undefined
    : Object.entries(shift.value).reduce(
        (enriched, [dayName, dayTimes]) => ({
          ...enriched,
          [dayName]: Object.entries(dayTimes).reduce(
            (times, [timeName, timeUsers]) => ({
              ...times,
              [timeName]: timeUsers.map((userId) =>
                userList.value.find((user) => user.id === userId)
              )
            }),
            {}
          )
        }),
        {} as EnrichedShift
      )
)
const pickedShifts = computed(() =>
  Object.entries(enrichedShift.value ?? {}).reduce(
    (acc, [day, times]) => [
      ...acc,
      ...(times.morning.some((user) => user.id === loggedUser.value?.id)
        ? [{ day, time: 'morning' } as ShiftSelection]
        : []),
      ...(times.afternoon.some((user) => user.id === loggedUser.value?.id)
        ? [{ day, time: 'afternoon' } as ShiftSelection]
        : [])
    ],
    [] as ShiftSelection[]
  )
)

function handleShiftSelect(selectedShift: ShiftSelection) {
  if (!loggedUser.value) return

  if (
    enrichedShift.value?.[selectedShift.day][selectedShift.time]
      .map((user) => user.id)
      .includes(loggedUser.value.id)
  ) {
    shiftStore.sendShiftAction('remove_user', loggedUser.value.id, selectedShift)
    return
  }

  shiftStore.sendShiftAction('add_user', loggedUser.value.id, selectedShift)
}

async function handleCleanShift() {
  try {
    await shiftStore.cleanShift()
    showSuccessNotification('El turno ha sido reiniciado correctamente.')
  } catch (error) {
    showErrorNotification('Un error inesperado ocurrió intentando reiniciar el turno.')
  }
}

async function handleToggleStatus() {
  try {
    await shiftStore.toggleStatus()
  } catch (error) {
    showErrorNotification('Un error inesperado ocurrió intentando actualizar el estado del turno.')
  }
}

onBeforeMount(async () => {
  isLoading.value = true

  await userStore.fetchUsers()
  shiftStore.startConnection()

  isLoading.value = false
})

onBeforeUnmount(() => {
  shiftStore.finishConnection()
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificationsRef" />

    <AppHeader title="Cuadrante de turnos">
      <button v-if="!status || isLoading || isConnecting" class="btn btn-square btn-ghost">
        <span class="loading loading-dots text-3xl" />
      </button>
      <button v-else class="btn btn-square btn-ghost" @click="handleToggleStatus">
        <span
          :class="[
            'text-3xl',
            status === 'open' ? 'i-mingcute-pause-line' : 'i-mingcute-play-line text-3xl'
          ]"
        />
      </button>
      <button class="btn btn-square btn-ghost" @click="handleCleanShift">
        <span class="i-mingcute-file-new-line text-3xl" />
      </button>
    </AppHeader>

    <div
      v-if="isLoading || isConnecting || !enrichedShift || !status"
      class="flex h-full w-full items-center justify-center"
    >
      <span class="loading loading-spinner loading-lg text-secondary" />
    </div>

    <section v-else class="mt-2 min-h-0 w-full flex-grow overflow-y-auto px-6 pb-8">
      <div class="mb-3 flex justify-between px-1">
        <div class="flex items-center gap-2">
          <span class="i-mingcute-group-fill text-2xl text-secondary" />
          <p class="font-semibold">{{ connections }}</p>
        </div>

        <div class="flex min-w-28 items-center gap-2">
          <p class="font-semibold">Estado</p>
          <ShiftStatus :status="status" class="w-full" />
        </div>
      </div>

      <ShiftPicker
        :weekly-shift="enrichedShift"
        :picked-shifts="pickedShifts"
        @select-shift="handleShiftSelect"
      />
    </section>
  </main>
</template>
