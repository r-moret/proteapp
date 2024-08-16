<script setup lang="ts">
import type { EnrichedShift, WeekDay, ShiftTime } from '../declarations'
import ShiftSigner from './ShiftSigner.vue'

type PickedShift = { day: WeekDay; time: ShiftTime }

const TIMES = ['morning', 'afternoon'] as const
const DAYS: Record<WeekDay, string> = {
  monday: 'lunes',
  thursday: 'martes',
  wednesday: 'miércoles',
  tuesday: 'jueves',
  friday: 'viernes',
  saturday: 'sábado',
  sunday: 'domingo'
}

const props = defineProps<{
  weeklyShift: EnrichedShift
  pickedShifts: PickedShift[]
}>()

const emit = defineEmits<{
  selectShift: [payload: PickedShift]
}>()
</script>

<template>
  <div class="flex flex-col gap-5">
    <div v-for="(name, day) in DAYS" :key="day" class="flex flex-col gap-2">
      <header class="text-2xl font-semibold first-letter:uppercase">{{ name }}</header>
      <div class="grid grid-cols-2 gap-7 px-2">
        <ShiftSigner
          v-for="time in TIMES"
          :key="time"
          :users="props.weeklyShift[day][time]"
          :max-users="2"
          :highlight="props.pickedShifts.some((shift) => shift.day === day && shift.time === time)"
          :time="time"
          class="aspect-square"
          @select="emit('selectShift', { day, time })"
        />
      </div>
    </div>
  </div>
</template>
