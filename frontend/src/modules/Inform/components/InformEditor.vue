<script setup lang="ts">
import type { EditInform, UserInfo } from '@/modules/Inform/declarations'
import { ref } from 'vue'
import { useUserStore } from '@/store/UserStore'
import { useAnimalStore } from '@/store/AnimalStore'
import { useYardStore } from '@/store/YardStore'
import { storeToRefs } from 'pinia'
import UserCard from '@/modules/Inform/components/UserCard.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import ItemSelector from '@/components/ItemSelector.vue'
import HoursInput from '@/components/HoursInput.vue'
import DateInput from '@/components/DateInput.vue'
import TextListInput from '@/components/TextListInput.vue'
import type { AnimalInfo } from '@/modules/Animal/declarations'
import AnimalNotesEditor from '@/components/AnimalNotesEditor.vue'
import AnimalSelector from './AnimalSelector.vue'
import DropdownSelector from '@/components/DropdownSelector.vue'
import AdoptionCard from '@/modules/Adoption/components/AdoptionCard.vue'
import AnimalTestCard from '@/modules/Inform/components/AnimalTestCard.vue'
import AnimalCard from '@/modules/Animal/components/AnimalCard.vue'
import MultipleTextListInput from '@/components/MultipleTextListInput.vue'
import TextInput from '@/components/TextInput.vue'
import { toLocal } from '@/utils'
import { format } from '@formkit/tempo'
import type { Optional } from '@/types'
import type {
  EnrichedInform,
  EnrichedFields,
  Visit,
  Arrival,
  Adoption,
  AnimalTest,
  Loss
} from '@/modules/Inform/declarations'

const { userList } = storeToRefs(useUserStore())
const { animalList } = storeToRefs(useAnimalStore())
const { yardList } = storeToRefs(useYardStore())

const props = defineProps<{
  modelValue: EditInform
}>()

const emit = defineEmits<{
  'update:model-value': [payload: EditInform]
}>()

const enrichedInform = ref<EnrichedInform>({
  creator: userList.value.find((user) => user.id === props.modelValue.creator)!, // TODO
  volunteers: props.modelValue.volunteers.map(
    (vol) => userList.value.find((user) => user.id === vol)! // TODO
  ),
  date: props.modelValue.date,
  timeRange: [
    {
      hours: toLocal(props.modelValue.timeRange.start).getHours(),
      minutes: toLocal(props.modelValue.timeRange.start).getMinutes()
    },
    {
      hours: toLocal(props.modelValue.timeRange.end).getHours(),
      minutes: toLocal(props.modelValue.timeRange.end).getMinutes()
    }
  ],
  highlights: props.modelValue.highlights,
  notes: animalList.value.map((animal) => ({ info: animal })),
  adoptions: props.modelValue.adoptions.map((adop) => ({
    animal: animalList.value.find((animal) => animal.id === adop.animal)!, // TODO
    foster: adop.foster
  })),
  testedAnimals: props.modelValue.testedAnimals.map((test) => ({
    animal: animalList.value.find((animal) => animal.id === test.animal)!, // TODO
    compatible: test.compatible
  })),
  losses: props.modelValue.losses.map((loss) => ({
    animal: animalList.value.find((animal) => animal.id === loss.animal)! // TODO
  })),
  visits: props.modelValue.visits,
  arrivals: props.modelValue.arrivals
})

const newAdoption = ref<Optional<Adoption, 'animal'>>({
  animal: undefined,
  foster: false
})
const newAnimalTest = ref<Optional<AnimalTest, 'animal'>>({
  animal: undefined,
  compatible: false
})
const newLoss = ref<Partial<Loss>>({
  animal: undefined
})
const newVisit = ref<Partial<Visit>>({
  visitor: undefined,
  description: undefined
})
const newArrival = ref<Partial<Arrival>>({
  name: undefined,
  description: undefined
})

const volunteersDrawerOpen = ref(false)
const adoptionsDrawerOpen = ref(false)
const newAnimalTestDrawerOpen = ref(false)
const newLossDrawerOpen = ref(false)
const newVisitDrawerOpen = ref(false)
const newArrivalDrawerOpen = ref(false)

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
    case 'timeRange': {
      const start = new Date()
      const end = new Date()

      start.setHours(update[0].hours, update[0].minutes, 0)
      end.setHours(update[1].hours, update[1].minutes, 0)

      modelUpdate = {
        start: format(start, 'HH:mm:ssZ'),
        end: format(end, 'HH:mm:ssZ')
      }
      break
    }
    case 'highlights':
      modelUpdate = update
      break
    case 'notes':
      modelUpdate = update
        ?.filter((note) => note.note)
        .map((note) => ({ animal: note.info.id, text: note.note }))
      break
    case 'adoptions':
      modelUpdate = update?.map((adop) => ({ animal: adop.animal.id, foster: adop.foster }))
      break
    case 'testedAnimals':
      modelUpdate = update?.map((test) => ({ animal: test.animal.id, compatible: test.compatible }))
      break
    case 'losses':
      modelUpdate = update?.map((test) => ({ animal: test.animal.id }))
      break
    case 'visits':
      modelUpdate = update
      break
    case 'arrivals':
      modelUpdate = update
      break
    default:
      return
  }

  enrichedInform.value = { ...enrichedInform.value, [field]: update }
  emit('update:model-value', {
    ...props.modelValue,
    [field]: modelUpdate
  })
}

function handleAddNoteInHighlights(highlight: string) {
  handleFieldUpdate('highlights', [...(props.modelValue.highlights ?? []), highlight])
}

function handleAddToAnimalListField(
  listField: 'adoptions' | 'testedAnimals' | 'losses',
  callback: () => void
) {
  const duplicatedAnimal = (newAnimal: AnimalInfo) =>
    !!enrichedInform.value[listField]?.some((animalItem) => animalItem.animal.id === newAnimal.id)

  switch (listField) {
    case 'adoptions':
      if (!newAdoption.value.animal) return // TODO: Notification
      if (duplicatedAnimal(newAdoption.value.animal)) return // TODO: Notification
      handleFieldUpdate('adoptions', [
        ...(enrichedInform.value[listField] ?? []),
        { ...newAdoption.value, animal: newAdoption.value.animal! }
      ])
      break
    case 'testedAnimals':
      if (!newAnimalTest.value.animal) return // TODO: Notification
      if (duplicatedAnimal(newAnimalTest.value.animal)) return // TODO: Notification
      handleFieldUpdate('testedAnimals', [
        ...(enrichedInform.value[listField] ?? []),
        { ...newAnimalTest.value, animal: newAnimalTest.value.animal! }
      ])
      break
    default:
      if (!newLoss.value.animal) return // TODO: Notification
      if (duplicatedAnimal(newLoss.value.animal)) return // TODO: Notification
      handleFieldUpdate('losses', [
        ...(enrichedInform.value[listField] ?? []),
        { ...newLoss.value, animal: newLoss.value.animal! }
      ])
      break
  }

  callback()
}

function handleRemoveFromAnimalListField(
  ...animalListItem:
    | ['adoptions', { animal: AnimalInfo; foster: boolean }]
    | ['testedAnimals', { animal: AnimalInfo; compatible: boolean }]
    | ['losses', { animal: AnimalInfo }]
) {
  switch (animalListItem[0]) {
    case 'adoptions':
      handleFieldUpdate(
        'adoptions',
        (enrichedInform.value.adoptions ?? []).filter(
          (saved) => saved.animal.id !== animalListItem[1].animal.id
        )
      )
      break
    case 'testedAnimals':
      handleFieldUpdate(
        'testedAnimals',
        (enrichedInform.value.testedAnimals ?? []).filter(
          (saved) => saved.animal.id !== animalListItem[1].animal.id
        )
      )
      break
    default:
      handleFieldUpdate(
        'losses',
        (enrichedInform.value.losses ?? []).filter(
          (saved) => saved.animal.id !== animalListItem[1].animal.id
        )
      )
      break
  }
}

function handleCreateVisit(visitor: string) {
  newVisit.value = { visitor, description: undefined }
  newVisitDrawerOpen.value = true
}

function handleCreateArrival(name: string) {
  newArrival.value = { name, description: undefined }
  newArrivalDrawerOpen.value = true
}
</script>

<template>
  <div>
    <div class="flex flex-col gap-8 pb-8">
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
          :editable="true"
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
          :editable="true"
          @add-highlight="handleAddNoteInHighlights"
          @update:model-value="(notes) => handleFieldUpdate('notes', notes)"
        />
      </div>

      <div class="flex flex-col gap-4">
        <div class="collapse collapse-arrow">
          <input class="min-h-0" type="checkbox" />
          <div class="collapse-title min-h-0 p-0 text-xl font-medium after:-mt-[1rem]">
            <h2 class="flex items-center gap-4">
              <p class="text-xl font-semibold">Adopciones</p>
              <p class="badge badge-secondary badge-lg">
                {{ enrichedInform.adoptions?.length ?? 0 }}
              </p>
            </h2>
          </div>
          <div class="collapse-content px-0 !pb-0">
            <p v-if="!enrichedInform.adoptions?.length" class="mt-4 text-center italic">
              No hay adopciones
            </p>
            <ul v-else class="mt-4 flex flex-col gap-2">
              <li v-for="adoption in enrichedInform.adoptions" :key="adoption.animal.id">
                <AdoptionCard :adoption size="compact">
                  <template #action>
                    <span
                      class="i-mingcute-close-fill"
                      @click="handleRemoveFromAnimalListField('adoptions', adoption)"
                    />
                  </template>
                </AdoptionCard>
              </li>
            </ul>
          </div>
        </div>

        <button
          class="w-full rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
          @click="adoptionsDrawerOpen = true"
        >
          Añadir adopción
        </button>
      </div>

      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Visitas</h2>
        <MultipleTextListInput
          :model-value="enrichedInform.visits"
          :editable="true"
          placeholder="Ej. Una pareja joven de veintipico años"
          @add="handleCreateVisit"
          @update:model-value="(visits: Visit[]) => handleFieldUpdate('visits', visits)"
        >
          <template #inputIcon>
            <span class="i-mingcute-group-fill text-2xl text-secondary" />
          </template>
          <template #empty>
            <p class="my-1 text-center italic text-gray-400">No hay visitas</p>
          </template>
          <template #item="{ item }">
            <div class="flex flex-col gap-1">
              <p class="font-semibold">{{ item.visitor }}</p>
              <p class="italic">{{ item.description }}</p>
            </div>
          </template>
        </MultipleTextListInput>
      </div>

      <div class="flex flex-col gap-4">
        <div class="collapse collapse-arrow">
          <input class="min-h-0" type="checkbox" />
          <div class="collapse-title min-h-0 p-0 text-xl font-medium after:-mt-[1rem]">
            <h2 class="flex items-center gap-4">
              <p class="text-xl font-semibold">Pruebas de animales</p>
              <p class="badge badge-secondary badge-lg">
                {{ enrichedInform.testedAnimals?.length ?? 0 }}
              </p>
            </h2>
          </div>
          <div class="collapse-content px-0 !pb-0">
            <p v-if="!enrichedInform.testedAnimals?.length" class="mt-4 text-center italic">
              No hay pruebas de animales
            </p>
            <ul v-else class="mt-4 flex flex-col gap-2">
              <li v-for="animalTest in enrichedInform.testedAnimals" :key="animalTest.animal.id">
                <AnimalTestCard :animalTest>
                  <template #action>
                    <span
                      class="i-mingcute-close-fill"
                      @click="handleRemoveFromAnimalListField('testedAnimals', animalTest)"
                    />
                  </template>
                </AnimalTestCard>
              </li>
            </ul>
          </div>
        </div>

        <button
          class="w-full rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
          @click="newAnimalTestDrawerOpen = true"
        >
          Añadir prueba de animal
        </button>
      </div>

      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Entradas</h2>
        <MultipleTextListInput
          :model-value="enrichedInform.arrivals"
          :editable="true"
          placeholder="Ej. Zelda"
          @add="handleCreateArrival"
          @update:model-value="(arrivals: Arrival[]) => handleFieldUpdate('arrivals', arrivals)"
        >
          <template #inputIcon>
            <span class="i-mingcute-cat-fill text-2xl text-secondary" />
          </template>
          <template #empty>
            <p class="my-1 text-center italic text-gray-400">No hay entradas</p>
          </template>
          <template #item="{ item }">
            <div class="flex flex-col gap-1">
              <p class="font-semibold">{{ item.name }}</p>
              <p class="italic">{{ item.description }}</p>
            </div>
          </template>
        </MultipleTextListInput>
      </div>

      <div class="flex flex-col gap-4">
        <div class="collapse collapse-arrow">
          <input class="min-h-0" type="checkbox" />
          <div class="collapse-title min-h-0 p-0 text-xl font-medium after:-mt-[1rem]">
            <h2 class="flex items-center gap-4">
              <p class="text-xl font-semibold">Pérdidas</p>
              <p class="badge badge-secondary badge-lg">
                {{ enrichedInform.losses?.length ?? 0 }}
              </p>
            </h2>
          </div>
          <div class="collapse-content px-0 !pb-0">
            <p v-if="!enrichedInform.losses?.length" class="mt-4 text-center italic">
              No hay pérdidas
            </p>
            <ul v-else class="mt-4 flex flex-col gap-2">
              <li v-for="loss in enrichedInform.losses" :key="loss.animal.id">
                <AnimalCard :animal="loss.animal" size="compact">
                  <template #action>
                    <span
                      class="i-mingcute-close-fill"
                      @click="handleRemoveFromAnimalListField('losses', loss)"
                    />
                  </template>
                </AnimalCard>
              </li>
            </ul>
          </div>
        </div>

        <button
          class="w-full rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
          @click="newLossDrawerOpen = true"
        >
          Añadir pérdida
        </button>
      </div>
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
                @click="handleAddToAnimalListField('adoptions', close)"
              >
                Crear
              </button>
            </div>
          </div>
        </div>
      </template>
    </BottomDrawer>

    <BottomDrawer
      class="bg-base-200"
      size="small"
      v-model="newAnimalTestDrawerOpen"
      @close="newAnimalTest = { animal: undefined, compatible: false }"
    >
      <template #default="{ close }">
        <div class="flex h-full flex-col gap-5">
          <h1 class="text-3xl font-semibold">Nueva prueba de compatibilidad</h1>
          <div class="flex flex-col gap-4">
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Animal</h2>
              <AnimalSelector v-model="newAnimalTest.animal" />
            </section>
            <section class="flex w-full flex-col gap-2">
              <h2 class="text-xl font-semibold">Compatibilidad</h2>
              <DropdownSelector
                :items="['No es compatible', 'Es compatible']"
                class="w-full"
                @select="
                  (compatibility) => {
                    newAnimalTest.compatible = compatibility === 'Es compatible'
                  }
                "
              >
                <template #button>
                  <button
                    class="flex w-full items-center justify-center gap-2 rounded-xl bg-secondary-content px-4 py-2 font-semibold text-neutral"
                  >
                    {{ newAnimalTest.compatible ? 'Es compatible' : 'No es compatible' }}
                    <span class="i-mingcute-down-fill text-xl" />
                  </button>
                </template>
              </DropdownSelector>
            </section>
            <div class="mt-10 flex justify-center">
              <button
                class="w-fit items-center justify-center rounded-lg bg-secondary px-10 py-2 font-semibold text-white"
                :disabled="!newAnimalTest.animal"
                @click="handleAddToAnimalListField('testedAnimals', close)"
              >
                Crear
              </button>
            </div>
          </div>
        </div>
      </template>
    </BottomDrawer>

    <BottomDrawer
      class="bg-base-200"
      size="tiny"
      v-model="newLossDrawerOpen"
      @close="newLoss = { animal: undefined }"
    >
      <template #default="{ close }">
        <div class="flex h-full flex-col gap-5">
          <h1 class="text-3xl font-semibold">Nueva pérdida</h1>
          <div class="flex flex-col gap-4">
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Animal</h2>
              <AnimalSelector v-model="newLoss.animal" />
            </section>
            <div class="mt-8 flex justify-center">
              <button
                class="w-fit items-center justify-center rounded-lg bg-secondary px-10 py-2 font-semibold text-white"
                :disabled="!newLoss.animal"
                @click="handleAddToAnimalListField('losses', close)"
              >
                Crear
              </button>
            </div>
          </div>
        </div>
      </template>
    </BottomDrawer>

    <BottomDrawer
      class="bg-base-200"
      size="small"
      v-model="newVisitDrawerOpen"
      @close="newVisit = { visitor: undefined, description: undefined }"
    >
      <template #default="{ close }">
        <div class="flex h-full flex-col gap-5">
          <h1 class="text-3xl font-semibold">Nueva visita</h1>
          <div class="flex flex-col gap-4">
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Visitante</h2>
              <TextInput v-model="newVisit.visitor" />
            </section>
            <section class="flex w-full flex-col gap-2">
              <h2 class="text-xl font-semibold">Descripción de la visita</h2>
              <TextInput
                v-model="newVisit.description"
                placeholder="Ej. Pareja muy concienciada con la seguridad del animal..."
              />
            </section>
            <div class="mt-10 flex justify-center">
              <button
                class="w-fit items-center justify-center rounded-lg bg-secondary px-10 py-2 font-semibold text-white"
                :disabled="!newVisit.visitor || !newVisit.description"
                @click="
                  () => {
                    handleFieldUpdate('visits', [
                      ...(enrichedInform.visits ?? []),
                      { visitor: newVisit.visitor!, description: newVisit.description! }
                    ])
                    close()
                  }
                "
              >
                Crear
              </button>
            </div>
          </div>
        </div>
      </template>
    </BottomDrawer>

    <BottomDrawer
      class="bg-base-200"
      size="small"
      v-model="newArrivalDrawerOpen"
      @close="newArrival = { name: undefined, description: undefined }"
    >
      <template #default="{ close }">
        <div class="flex h-full flex-col gap-5">
          <h1 class="text-3xl font-semibold">Nueva entrada</h1>
          <div class="flex flex-col gap-4">
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Animal</h2>
              <TextInput v-model="newArrival.name" />
            </section>
            <section class="flex w-full flex-col gap-2">
              <h2 class="text-xl font-semibold">Descripción del animal</h2>
              <TextInput
                v-model="newArrival.description"
                placeholder="Ej. Gatito de unos dos meses con el pelo naranja"
              />
            </section>
            <div class="mt-10 flex justify-center">
              <button
                class="w-fit items-center justify-center rounded-lg bg-secondary px-10 py-2 font-semibold text-white"
                :disabled="!newArrival.name"
                @click="
                  () => {
                    handleFieldUpdate('arrivals', [
                      ...(enrichedInform.arrivals ?? []),
                      { name: newArrival.name!, description: newArrival.description! }
                    ])
                    close()
                  }
                "
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
