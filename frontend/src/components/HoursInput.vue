<script setup lang="ts">
import Datepicker from '@vuepic/vue-datepicker'

type Time = { hours: number; minutes: number }

const model = defineModel<[Time, Time]>({ required: true })

const props = withDefaults(
  defineProps<{
    clearable?: boolean
    includeIcon?: boolean
  }>(),
  {
    includeIcon: true
  }
)
</script>

<template>
  <div class="flex h-12 w-full">
    <template v-if="props.includeIcon">
      <div class="flex items-center justify-center rounded-l-lg bg-white px-3">
        <span class="i-mingcute-time-fill text-2xl text-secondary" />
      </div>
      <div class="divider divider-horizontal mx-0 w-fit bg-white py-2" />
    </template>
    <Datepicker
      class="w-full"
      v-model="model"
      auto-apply
      hide-input-icon
      time-picker
      :range="true"
      locale="es-ES"
      :clearable="props.clearable"
      :ui="{
        menu: 'hours-menu',
        input: 'hours-input'
      }"
    />
  </div>
</template>

<style>
.hours-menu {
  border-radius: 1.5rem;
  overflow: hidden;
}

.hours-input {
  height: 3rem;
  border: none;
  border-radius: v-bind('props.includeIcon ? "0 0.5rem 0.5rem 0" : "0.5rem"');
}

.dp__theme_light {
  --dp-primary-color: oklch(var(--s));
}
</style>
