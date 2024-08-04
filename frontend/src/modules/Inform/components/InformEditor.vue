<script setup lang="ts">
import type { EditInform, UserInfo } from '@/modules/Inform/declarations'
import { ref } from 'vue'
import { useUserStore } from '@/store/UserStore'
import { useAnimalStore } from '@/store/AnimalStore'
import { storeToRefs } from 'pinia'
import UserCard from '@/modules/Inform/components/UserCard.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import ItemSelector from '@/components/ItemSelector.vue'
import HoursInput from '@/components/HoursInput.vue'
import DateInput from '@/components/DateInput.vue'
import TextListInput from '@/components/TextListInput.vue'
import { pick } from 'lodash'
import type { AnimalInfo } from '@/modules/Animal/declarations'
import AnimalNotesEditor from '@/components/AnimalNotesEditor.vue'
import AnimalSelector from './AnimalSelector.vue'
import DropdownSelector from '@/components/DropdownSelector.vue'
import AdoptionCard from '@/modules/Adoption/components/AdoptionCard.vue'

const { userList } = storeToRefs(useUserStore())
const { yardList, animalList } = storeToRefs(useAnimalStore())

const props = defineProps<{
  modelValue: EditInform
}>()

const emit = defineEmits<{
  'update:model-value': [payload: EditInform]
}>()

type TimeRange = [{ hours: number; minutes: number }, { hours: number; minutes: number }]
type EnrichedFields =
  | ['creator', UserInfo]
  | ['volunteers', UserInfo[]]
  | ['date', Date]
  | ['timeRange', TimeRange]
  | ['highlights', string[] | undefined | null]
  | ['notes', { info: AnimalInfo; note?: string }[]]
  | ['adoptions', { animal: AnimalInfo; foster: boolean }[]]
type EnrichedInform = { [key in EnrichedFields[0]]: Extract<EnrichedFields, [key, any]>[1] }

const enrichedInform = ref<EnrichedInform>({
  creator: userList.value.find((user) => user.id === props.modelValue.creator)!, // TODO
  volunteers: props.modelValue.volunteers.map(
    (vol) => userList.value.find((user) => user.id === vol)! // TODO
  ),
  date: props.modelValue.date,
  timeRange: [props.modelValue.timeRange.start, props.modelValue.timeRange.end],
  highlights: props.modelValue.highlights,
  notes: animalList.value.map((animal) => ({ info: animal })),
  adoptions: props.modelValue.adoptions.map((adop) => ({
    animal: animalList.value.find((animal) => animal.id === adop.animal)!, // TODO
    foster: adop.foster
  }))
})

const newAdoption = ref<{
  animal?: AnimalInfo
  foster: boolean
}>({
  animal: undefined,
  foster: false
})

const volunteersDrawerOpen = ref(false)
const adoptionsDrawerOpen = ref(false)

function handleFieldUpdate(...[field, update]: EnrichedFields) {
  let modelUpdate: EditInform[keyof EditInform]

  switch (field) {
    case 'creator':
      modelUpdate = update.id
      break
    case 'volunteers':
      modelUpdate = update.map((user) => user.id)
      break
    case 'date':
      modelUpdate = update
      break
    case 'timeRange':
      modelUpdate = {
        start: pick(update[0], ['hours', 'minutes']),
        end: pick(update[1], ['hours', 'minutes'])
      }
      break
    case 'highlights':
      modelUpdate = update
      break
    case 'notes':
      modelUpdate = update
        .filter((note) => note.note)
        .map((note) => ({ animal: note.info.id, text: note.note }))
      break
    case 'adoptions':
      modelUpdate = update.map((adop) => ({ animal: adop.animal.id, foster: adop.foster }))
      break
    default:
      return
  }

  enrichedInform.value = { ...enrichedInform.value, [field]: update }
  console.log({
    ...props.modelValue,
    [field]: modelUpdate
  })
  emit('update:model-value', {
    ...props.modelValue,
    [field]: modelUpdate
  })
}

function handleAddNoteInHighlights(highlight: string) {
  handleFieldUpdate('highlights', [...(props.modelValue.highlights ?? []), highlight])
}

function handleAddAdoption(callback: () => void) {
  if (
    enrichedInform.value.adoptions.some(
      (adoption) => adoption.animal.id === newAdoption.value.animal?.id
    )
  ) {
    // Show notification: This animal is already noted as adopted!
    return
  }

  handleFieldUpdate('adoptions', [
    ...enrichedInform.value.adoptions,
    { ...newAdoption.value, animal: newAdoption.value.animal! }
  ])

  callback()
}

function handleRemoveAdoption(adoption: { animal: AnimalInfo; foster: boolean }) {
  const newAdoptions = enrichedInform.value.adoptions.filter(
    (savedAdoption) => savedAdoption.animal.id !== adoption.animal.id
  )
  handleFieldUpdate('adoptions', newAdoptions)
}
</script>

<template>
  <div>
    <div class="flex flex-col gap-4">
      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Creador</h2>
        <UserCard size="compact" :user="enrichedInform.creator" />
      </div>

      <div>
        <div class="collapse collapse-arrow mb-4">
          <input class="min-h-0" type="checkbox" />
          <div class="collapse-title min-h-0 p-0 text-xl font-medium after:-mt-[1rem]">
            <h2 class="flex items-center gap-4">
              <p class="text-xl font-semibold">Voluntarios</p>
              <p class="badge badge-secondary badge-lg">{{ enrichedInform.volunteers.length }}</p>
            </h2>
          </div>
          <div class="collapse-content px-0 !pb-0">
            <p v-if="!enrichedInform.volunteers.length" class="mt-4 text-center italic">
              No hay voluntarios seleccionados
            </p>
            <div v-else class="mt-4 flex flex-col gap-2">
              <UserCard
                v-for="volunteer in enrichedInform.volunteers"
                size="compact"
                :user="volunteer"
                :key="volunteer.id"
              />
            </div>
          </div>
        </div>

        <button
          class="w-full rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
          @click="volunteersDrawerOpen = true"
        >
          Seleccionar voluntarios
        </button>
      </div>

      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Fecha</h2>
        <div class="flex gap-2">
          <div class="w-1/2">
            <DateInput
              :model-value="enrichedInform.date"
              :include-time="false"
              :clearable="false"
              date-format="short"
              @update:model-value="(date) => handleFieldUpdate('date', date!)"
            />
          </div>
          <div class="w-1/2">
            <HoursInput
              :model-value="enrichedInform.timeRange"
              @update:model-value="(times) => handleFieldUpdate('timeRange', times)"
            />
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Destacado</h2>
        <TextListInput
          :model-value="enrichedInform.highlights"
          placeholder="El turno de hoy fue..."
          @update:model-value="(highlights) => handleFieldUpdate('highlights', highlights)"
        >
          <template #empty>
            <p class="my-1 text-center italic text-gray-400">No hay notas destacadas</p>
          </template>
        </TextListInput>
      </div>

      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Notas</h2>
        <AnimalNotesEditor
          :yards="yardList"
          :model-value="enrichedInform.notes"
          @add-highlight="handleAddNoteInHighlights"
          @update:model-value="(notes) => handleFieldUpdate('notes', notes)"
        />
      </div>

      <div class="flex flex-col gap-4">
        <p class="text-xl font-semibold">Adopciones</p>
        <p v-if="!enrichedInform.adoptions.length" class="text-center italic">No hay adopciones</p>
        <ul v-else class="flex flex-col gap-2">
          <li v-for="adoption in enrichedInform.adoptions" :key="adoption.animal.id">
            <AdoptionCard :adoption size="compact">
              <template #action>
                <span class="i-mingcute-close-fill" @click="handleRemoveAdoption(adoption)" />
              </template>
            </AdoptionCard>
          </li>
        </ul>

        <button
          class="w-full rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
          @click="adoptionsDrawerOpen = true"
        >
          Añadir adopción
        </button>
      </div>

      <pre>{{ props.modelValue }}</pre>
    </div>

    <BottomDrawer class="bg-base-200" size="medium" v-model="volunteersDrawerOpen">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Voluntarios</h1>
        <div class="flex flex-col gap-2">
          <ItemSelector
            :items="userList"
            :model-value="enrichedInform.volunteers"
            :include-search="true"
            :search-fn="
              (user) =>
                `${user.person.name} ${user.person.firstSurname} ${user.person.secondSurname ?? ''}`
            "
            @update:model-value="
              (selectedVolunteers: UserInfo[]) =>
                handleFieldUpdate('volunteers', selectedVolunteers)
            "
          >
            <template #item="{ item, isSelected, toggleSelect }">
              <UserCard
                size="regular"
                :user="item"
                :class="[
                  'border-2',
                  isSelected ? 'border-secondary shadow-secondary' : 'border-transparent'
                ]"
                @click="toggleSelect(item)"
              />
            </template>
          </ItemSelector>
        </div>
      </div>
    </BottomDrawer>

    <BottomDrawer
      class="bg-base-200"
      size="small"
      v-model="adoptionsDrawerOpen"
      @close="newAdoption = { animal: undefined, foster: false }"
    >
      <template #default="{ close }">
        <div class="flex h-full flex-col gap-5">
          <h1 class="text-3xl font-semibold">Nueva adopción</h1>
          <div class="flex flex-col gap-4">
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Animal</h2>
              <AnimalSelector v-model="newAdoption.animal" />
            </section>
            <section class="flex w-full flex-col gap-2">
              <h2 class="text-xl font-semibold">Tipo de adopción</h2>
              <DropdownSelector
                :items="['Permanente', 'Casa de acogida']"
                class="w-full"
                @select="
                  (adoptionType) => {
                    newAdoption.foster = adoptionType === 'Casa de acogida'
                  }
                "
              >
                <template #button>
                  <button
                    class="flex w-full items-center justify-center gap-2 rounded-xl bg-secondary-content px-4 py-2 font-semibold text-neutral"
                  >
                    {{ newAdoption.foster ? 'Casa de acogida' : 'Permanente' }}
                    <span class="i-mingcute-down-fill text-xl" />
                  </button>
                </template>
              </DropdownSelector>
            </section>
            <div class="mt-10 flex justify-center">
              <button
                class="w-fit items-center justify-center rounded-lg bg-secondary px-10 py-2 font-semibold text-white"
                :disabled="!newAdoption.animal"
                @click="handleAddAdoption(close)"
              >
                Crear
              </button>
            </div>
          </div>
        </div>
      </template>
    </BottomDrawer>
  </div>
</template>
