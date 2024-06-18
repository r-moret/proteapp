<script setup lang="ts">
import Datepicker from '@vuepic/vue-datepicker'

import { format } from '@formkit/tempo'

const model = defineModel<Date>()

const dateFormatter = (date: Date) => {
  return format(date, { date: 'long' })
}
</script>

<template>
  <div class="flex h-12 w-full px-4">
    <div class="flex items-center justify-center rounded-l-lg bg-white px-3">
      <span class="i-mingcute-calendar-2-line text-2xl text-secondary" />
    </div>
    <div class="divider divider-horizontal mx-0 w-fit bg-white py-2" />
    <Datepicker
      class="w-full rounded-r-lg"
      v-model="model"
      auto-apply
      no-today
      hide-input-icon
      :enable-time-picker="false"
      locale="es-ES"
      placeholder="Selecciona una fecha"
      :format="dateFormatter"
      :ui="{
        menu: 'calendar-menu',
        input: 'calendar-input'
      }"
    />
  </div>
</template>

<style>
.calendar-menu {
  border-radius: 1.5rem;
}

.calendar-input {
  height: 3rem;
  border: none;
  border-radius: 0 0.5rem 0.5rem 0;
}

.dp__theme_light {
  --dp-primary-color: oklch(var(--s));
}
</style>
