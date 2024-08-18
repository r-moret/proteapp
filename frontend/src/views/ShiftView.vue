<script setup lang="ts">
import { onBeforeMount, ref, computed, onBeforeUnmount } from 'vue'
import { useUserStore } from '@/store/UserStore'
import { useShiftStore } from '@/store/ShiftStore'
import { storeToRefs } from 'pinia'

import AppHeader from '@/skeleton/AppHeader.vue'
import ShiftPicker from '@/modules/Shift/components/ShiftPicker.vue'
import ShiftStatus from '@/modules/Shift/components/ShiftStatus.vue'
import UserGroup from '@/components/UserGroup.vue'

import type { EnrichedShift, ShiftTime, WeekDay } from '@/modules/Shift/declarations'

const userStore = useUserStore()
const { userList, loggedUser } = storeToRefs(userStore)

const shiftStore = useShiftStore()
const { status, isConnecting } = storeToRefs(shiftStore)

const isLoading = ref(false)
const shift = ref<EnrichedShift>()

const pickedShifts = computed(() =>
  Object.entries(shift.value ?? {}).reduce(
    (acc, [day, times]) => [
      ...acc,
      ...(times.morning.some((user) => user.id === loggedUser.value?.id)
        ? [{ day, time: 'morning' } as { day: WeekDay; time: ShiftTime }]
        : []),
      ...(times.afternoon.some((user) => user.id === loggedUser.value?.id)
        ? [{ day, time: 'afternoon' } as { day: WeekDay; time: ShiftTime }]
        : [])
    ],
    [] as { day: WeekDay; time: ShiftTime }[]
  )
)

function handleShiftSelect(selectedShift: { day: WeekDay; time: ShiftTime }) {
  if (!loggedUser.value) return

  if (
    shift.value?.[selectedShift.day][selectedShift.time]
      .map((user) => user.id)
      .includes(loggedUser.value.id)
  ) {
    handleRemoveUserShift(loggedUser.value.id, selectedShift)
    return
  }

  handleAddUserShift(loggedUser.value.id, selectedShift)
}

function handleAddUserShift(userId: string, newShift: { day: WeekDay; time: ShiftTime }) {
  if (!shift.value) return

  const userInfo = userList.value.find((savedUser) => savedUser.id === userId)
  if (!userInfo) return // TODO

  shift.value[newShift.day][newShift.time].push(userInfo)
}

function handleRemoveUserShift(userId: string, oldShift: { day: WeekDay; time: ShiftTime }) {
  if (!shift.value) return

  shift.value[oldShift.day][oldShift.time] = shift.value[oldShift.day][oldShift.time].filter(
    (user) => user.id !== userId
  )
}

onBeforeMount(async () => {
  isLoading.value = true

  shiftStore.startConnection()
  await userStore.fetchUsers()

  shift.value = {
    monday: { morning: [userList.value[0], userList.value[0]], afternoon: [] },
    thursday: {
      morning: [userList.value[0], userList.value[1], userList.value[0], userList.value[1]],
      afternoon: [userList.value[0], userList.value[0]]
    },
    wednesday: {
      morning: [],
      afternoon: [userList.value[0], userList.value[1], userList.value[1]]
    },
    tuesday: { morning: [userList.value[1], userList.value[1]], afternoon: [] },
    friday: { morning: [userList.value[1]], afternoon: [userList.value[0], userList.value[1]] },
    saturday: {
      morning: [userList.value[0], userList.value[1]],
      afternoon: [userList.value[2], userList.value[2]]
    },
    sunday: {
      morning: [userList.value[2], userList.value[2], userList.value[2], userList.value[0]],
      afternoon: [userList.value[0]]
    }
  }

  isLoading.value = false
})

onBeforeUnmount(() => {
  shiftStore.finishConnection()
})
</script>

<template>
  <main class="flex flex-col">
    <AppHeader title="Cuadrante de turnos">
      <button class="btn btn-square btn-ghost">
        <span class="i-mingcute-more-1-line text-3xl" />
      </button>
      <button class="btn btn-square btn-ghost">
        <span class="i-mingcute-add-line text-3xl" />
      </button>
    </AppHeader>

    <div v-if="isLoading || isConnecting" class="flex h-full w-full items-center justify-center">
      <span class="loading loading-spinner loading-lg text-secondary" />
    </div>

    <section v-else class="min-h-0 w-full flex-grow overflow-y-auto px-6 pb-8">
      <div class="mb-3 flex justify-between px-1">
        <div class="flex flex-col justify-between">
          <p class="font-semibold">Conectados</p>
          <!-- userList is a placeholder -->
          <UserGroup :users="userList" :max="2" />
        </div>

        <div class="flex min-w-28 flex-col justify-between pb-1">
          <p class="font-semibold">Estado</p>
          <ShiftStatus :status="status ?? 'open'" class="w-full" />
        </div>
      </div>

      <ShiftPicker
        :weekly-shift="shift!"
        :picked-shifts="pickedShifts"
        @select-shift="handleShiftSelect"
      />
    </section>
  </main>
</template>
