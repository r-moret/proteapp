<script setup lang="ts">
import TextInput from '@/components/TextInput.vue'
import type { EditPerson } from '@/modules/Person/declarations'

const model = defineModel<EditPerson>()

const props = defineProps<{
  embedded?: boolean
}>()
</script>

<template>
  <div v-if="model" class="flex flex-col gap-4">
    <label class="flex flex-col gap-2">
      <span :class="['font-semibold', props.embedded ? 'text-md' : 'text-xl']">Nombre</span>
      <TextInput placeholder="Nombre de la persona" v-model="model.name" />
    </label>

    <div class="flex gap-4">
      <label class="flex flex-col gap-2">
        <span :class="['font-semibold', props.embedded ? 'text-md' : 'text-xl']"
          >Primer apellido</span
        >
        <TextInput placeholder="Primer apellido de la persona" v-model="model.firstSurname" />
      </label>
      <label class="flex flex-col gap-2">
        <span :class="['font-semibold', props.embedded ? 'text-md' : 'text-xl']"
          >Segundo apellido</span
        >
        <TextInput placeholder="Segundo apellido de la persona" v-model="model.secondSurname" />
      </label>
    </div>

    <label class="flex flex-col gap-2">
      <span :class="['font-semibold', props.embedded ? 'text-md' : 'text-xl']">Email</span>
      <TextInput placeholder="Correo electrónico" v-model="model.email" />
    </label>

    <label class="flex flex-col gap-2">
      <span :class="['font-semibold', props.embedded ? 'text-md' : 'text-xl']">Teléfono</span>
      <TextInput placeholder="Teléfono de contacto" v-model="model.phone" />
    </label>
  </div>
</template>
