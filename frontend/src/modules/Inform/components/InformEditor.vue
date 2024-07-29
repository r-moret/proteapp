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
type EnrichedInform = { [key in EnrichedFields[0]]: Extract<EnrichedFields, [key, any]>[1] }

const enrichedInform = ref<EnrichedInform>({
  creator: userList.value.find((user) => user.id === props.modelValue.creator)!, // TODO
  volunteers: props.modelValue.volunteers.map(
    (vol) => userList.value.find((user) => user.id === vol)! // TODO
  ),
  date: props.modelValue.date,
  timeRange: [props.modelValue.timeRange.start, props.modelValue.timeRange.end],
  highlights: props.modelValue.highlights,
  notes: animalList.value.map((animal) => ({ info: animal }))
})

const volunteersDrawerOpen = ref(false)

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
  </div>
</template>
