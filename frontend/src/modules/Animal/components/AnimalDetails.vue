<script setup lang="ts">
import { computed } from 'vue'
import { format } from '@formkit/tempo'

const props = defineProps<{
  isCastrated?: boolean | null
  isCompatible?: boolean | null
  birthDate?: Date | null
  location?: string | null
}>()

const details = computed(() => ({
  castration: {
    icon: props.isCastrated ? 'i-mingcute-lock-fill' : 'i-mingcute-unlock-line',
    label:
      props.isCastrated == undefined
        ? 'Desconocido'
        : props.isCastrated
          ? 'Castrado'
          : 'Sin castrar'
  },
  compatibility: {
    icon: props.isCompatible ? 'i-mingcute-paw-fill' : 'i-mingcute-paw-line',
    label:
      props.isCompatible == undefined
        ? 'Desconocido'
        : props.isCompatible
          ? 'Compatible con animales'
          : 'No compatible con animales'
  },
  location: {
    icon: 'i-mingcute-location-2-fill',
    label: props.location ?? 'Desconocido'
  },
  birth: {
    icon: 'i-mingcute-birthday-2-fill',
    label: props.birthDate == undefined ? 'Desconocido' : format(props.birthDate, 'medium', 'es-ES')
  }
}))
</script>

<template>
  <div class="flex justify-center gap-4 rounded-xl p-3">
    <div
      v-for="(detail, name) in details"
      :key="name"
      class="flex w-24 flex-col items-center gap-1"
    >
      <div class="relative flex text-3xl">
        <span
          v-if="name == 'compatibility' && !props.isCompatible"
          class="i-mingcute-line-fill absolute inset-0"
        />
        <span :class="detail.icon" />
      </div>
      <p class="text-center text-xs">{{ detail.label }}</p>
    </div>
  </div>
</template>
