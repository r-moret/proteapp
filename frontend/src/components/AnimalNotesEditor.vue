<script setup lang="ts">
import { type AnimalInfo, type YardInfo } from '@/modules/Animal/declarations'
import { computed, ref } from 'vue'
import BottomDrawer from './BottomDrawer.vue'
import TextInput from './TextInput.vue'

const model = defineModel<{ info: AnimalInfo; note?: string }[] | null>()

const props = defineProps<{
  yards: YardInfo[]
  editable?: boolean
}>()

const newNoteDrawerOpen = ref(false)
const viewNoteDrawerOpen = ref(false)
const newNote = ref<{
  animal?: AnimalInfo
  isOverwritting: boolean
  text: string
}>()
const selectedNote = ref<{
  animal: AnimalInfo
  text: string
}>()
const selectedYard = ref(props.yards[0].id)

const selectedYardAnimals = computed(
  () => model.value?.filter((animal) => animal.info.yard?.id === selectedYard.value) ?? []
)
const yardNumNotes = computed(() => {
  return props.yards.map((yard) => {
    return (model.value ?? [])
      .filter((animal) => animal.info.yard?.id === yard.id)
      .reduce((sum, animal) => {
        return sum + (animal.note ? 1 : 0)
      }, 0)
  })
})

function handleSelectAnimal(animal: { info: AnimalInfo; note?: string }) {
  if (props.editable) {
    newNoteDrawerOpen.value = true
    newNote.value = {
      animal: animal.info,
      isOverwritting: !!animal.note,
      text: animal.note ?? ''
    }
  } else {
    viewNoteDrawerOpen.value = true
    selectedNote.value = { animal: animal.info, text: animal.note ?? '' }
  }
}

function handleAddNote({ clear } = { clear: false }) {
  if (!newNote.value || !newNote.value.animal || !model.value) return

  if (clear) {
    newNote.value.text = ''
  }

  model.value = model.value.map((animal) =>
    animal.info.id === newNote.value?.animal?.id
      ? { info: newNote.value.animal, note: newNote.value.text }
      : animal
  )
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <div class="flex justify-center overflow-x-auto">
      <ul class="steps">
        <li
          v-for="(stepYard, index) in props.yards"
          :class="[
            'step',
            {
              'step-secondary':
                props.yards.findIndex((yard) => yard.id === stepYard.id) <=
                props.yards.findIndex((yard) => yard.id === selectedYard)
            }
          ]"
          :key="stepYard.id"
          @click="selectedYard = stepYard.id"
        >
          <div class="w-28">
            <div class="truncate">{{ stepYard.name }}</div>
            <div :class="['font-semibold', { invisible: yardNumNotes[index] === 0 }]">
              ({{ yardNumNotes[index] }} nota{{ yardNumNotes[index] > 1 ? 's' : '' }})
            </div>
          </div>
        </li>
      </ul>
    </div>
    <p v-if="selectedYardAnimals.length == 0" class="text-center italic text-gray-400">
      {{ props.editable ? 'Este patio está vacío' : 'No hay notas para animales de este patio' }}
    </p>
    <div v-else class="grid grid-cols-3 gap-y-4">
      <div
        v-for="animal in selectedYardAnimals"
        :class="[
          'mx-auto flex h-[4.5rem] w-[5.5rem] flex-col items-center justify-center rounded-xl border-2 bg-base-100 p-2',
          animal.note ? 'border-secondary shadow-sm shadow-secondary' : 'border-base-300'
        ]"
        :key="animal.info.id"
        @click="handleSelectAnimal(animal)"
      >
        <span
          :class="[
            'i-mingcute-cat-line text-3xl',
            animal.note ? 'text-secondary' : 'text-base-300'
          ]"
        />
        <p class="w-full truncate text-center text-neutral">{{ animal.info.name }}</p>
      </div>
    </div>
  </div>

  <BottomDrawer
    v-if="newNote && newNote.animal"
    class="bg-base-200"
    size="tiny"
    v-model="newNoteDrawerOpen"
  >
    <template #default="{ close }">
      <div class="flex h-full w-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Añadir nota a {{ newNote.animal.name }}</h1>
        <div class="flex flex-col items-center gap-6">
          <TextInput
            v-model="newNote.text"
            name="newNote"
            :placeholder="`Ej. A ${newNote.animal.name} se le ha aplicado su tratamiento...`"
          >
            <template #icon>
              <span class="i-mingcute-document-3-fill text-2xl text-secondary" />
            </template>
          </TextInput>
          <div class="flex gap-4">
            <button
              v-if="newNote.isOverwritting"
              class="w-fit rounded-lg border border-base-300 bg-secondary-content px-4 py-2 font-semibold text-base-content"
              @click="
                () => {
                  handleAddNote({ clear: true })
                  close()
                }
              "
            >
              Eliminar
            </button>
            <button
              class="w-fit rounded-lg bg-secondary px-4 py-2 font-semibold text-white"
              @click="
                () => {
                  handleAddNote()
                  close()
                }
              "
            >
              Añadir
            </button>
          </div>
        </div>
      </div>
    </template>
  </BottomDrawer>

  <BottomDrawer v-if="selectedNote" class="bg-base-200" size="tiny" v-model="viewNoteDrawerOpen">
    <template #default>
      <div class="flex h-full w-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Nota de {{ selectedNote.animal.name }}</h1>
        <div class="mb-4 flex gap-3 rounded-xl bg-white p-2">
          <span class="mt-4 font-serif text-7xl italic leading-10 text-gray-600">“</span>
          <p class="mt-3 text-lg italic">{{ selectedNote.text }}</p>
        </div>
      </div>
    </template>
  </BottomDrawer>
</template>
