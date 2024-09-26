<script setup lang="ts">
import type { EnrichedEditUser } from '@/modules/User/declarations'
import ImagePicker from '@/components/ImagePicker.vue'
import PersonEditor from '@/modules/Person/components/PersonEditor.vue'
import PersonSelector from '@/modules/Adoption/components/PersonSelector.vue'

const model = defineModel<Partial<EnrichedEditUser>>({ required: true })

const props = withDefaults(
  defineProps<{
    person: 'editor' | 'selector'
    showDetails?: boolean
  }>(),
  {
    showDetails: true
  }
)
</script>

<template>
  <div class="flex flex-col gap-4">
    <div class="flex flex-col gap-2">
      <h2 class="text-xl font-semibold">Imagen</h2>
      <ImagePicker v-model="model.image" class="px-2" />
    </div>

    <div class="flex flex-col gap-2">
      <h2 class="text-xl font-semibold">Persona</h2>
      <PersonEditor v-if="props.person === 'editor'" v-model="model.person" :embedded="true" />
      <PersonSelector v-else v-model="model.person" />
    </div>

    <div v-if="props.showDetails" class="flex flex-col gap-2">
      <h2 class="text-xl font-semibold">Detalles</h2>
      <label class="label gap-2">
        <input type="checkbox" class="checkbox-secondary checkbox" v-model="model.veteran" />
        <span class="label-text w-full text-start font-semibold"> Voluntario veterano </span>
      </label>
    </div>
  </div>
</template>
