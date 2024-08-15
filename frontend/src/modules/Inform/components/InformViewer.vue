<script setup lang="ts">
import type { EnrichedInform } from '@/modules/Inform/declarations'
import { useAnimalStore } from '@/store/AnimalStore'
import { storeToRefs } from 'pinia'
import UserCard from '@/modules/Inform/components/UserCard.vue'
import HoursInput from '@/components/HoursInput.vue'
import DateInput from '@/components/DateInput.vue'
import TextListInput from '@/components/TextListInput.vue'
import AnimalNotesEditor from '@/components/AnimalNotesEditor.vue'
import AdoptionCard from '@/modules/Adoption/components/AdoptionCard.vue'
import AnimalTestCard from '@/modules/Inform/components/AnimalTestCard.vue'
import AnimalCard from '@/modules/Animal/components/AnimalCard.vue'
import MultipleTextListInput from '@/components/MultipleTextListInput.vue'

const { yardList } = storeToRefs(useAnimalStore())

const props = defineProps<{
  inform: EnrichedInform
}>()
</script>

<template>
  <div>
    <div class="flex flex-col gap-6 pb-8">
      <div class="flex flex-col gap-4">
        <h2 class="text-xl font-semibold">Creador</h2>
        <UserCard size="compact" :user="props.inform.creator" />
      </div>

      <div class="flex flex-col gap-4">
        <h2>
          <p class="text-xl font-semibold">Voluntarios</p>
        </h2>
        <p v-if="!props.inform.volunteers.length" class="text-center italic text-gray-400">
          No hay más voluntarios
        </p>
        <div v-else class="flex flex-col gap-2">
          <UserCard
            v-for="volunteer in props.inform.volunteers"
            size="compact"
            :user="volunteer"
            :key="volunteer.id"
          />
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <h2 class="text-xl font-semibold">Fecha</h2>
        <div class="flex gap-2">
          <div class="w-1/2" @click.capture.stop>
            <DateInput
              :model-value="props.inform.date"
              :include-time="false"
              :clearable="false"
              date-format="short"
            />
          </div>
          <div class="w-1/2" @click.capture.stop>
            <HoursInput :model-value="props.inform.timeRange" />
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <h2 class="text-xl font-semibold">Destacado</h2>
        <TextListInput :model-value="props.inform.highlights" :editable="false">
          <template #empty>
            <p class="my-1 text-center italic text-gray-400">No hay notas destacadas</p>
          </template>
        </TextListInput>
      </div>

      <div class="flex flex-col gap-2">
        <h2 class="text-xl font-semibold">Notas</h2>
        <AnimalNotesEditor :yards="yardList" :model-value="props.inform.notes" :editable="false" />
      </div>

      <div class="flex flex-col gap-4">
        <h2>
          <p class="text-xl font-semibold">Adopciones</p>
        </h2>
        <p v-if="!props.inform.adoptions?.length" class="mt-2 text-center italic text-gray-400">
          No hay adopciones
        </p>
        <ul v-else class="flex flex-col gap-2">
          <li v-for="adoption in props.inform.adoptions" :key="adoption.animal.id">
            <AdoptionCard :adoption size="compact" />
          </li>
        </ul>
      </div>

      <div class="flex flex-col gap-4">
        <h2 class="text-xl font-semibold">Visitas</h2>
        <MultipleTextListInput :model-value="props.inform.visits" :editable="false">
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
        <h2>
          <p class="text-xl font-semibold">Pruebas de animales</p>
        </h2>
        <p v-if="!props.inform.testedAnimals?.length" class="mt-2 text-center italic text-gray-400">
          No hay pruebas de animales
        </p>
        <ul v-else class="flex flex-col gap-2">
          <li v-for="animalTest in props.inform.testedAnimals" :key="animalTest.animal.id">
            <AnimalTestCard :animalTest />
          </li>
        </ul>
      </div>

      <div class="flex flex-col gap-4">
        <h2 class="text-xl font-semibold">Entradas</h2>
        <MultipleTextListInput :model-value="props.inform.arrivals" :editable="false">
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
        <h2>
          <p class="text-xl font-semibold">Pérdidas</p>
        </h2>
        <p v-if="!props.inform.losses?.length" class="mt-2 text-center italic text-gray-400">
          No hay pérdidas
        </p>
        <ul v-else class="flex flex-col gap-2">
          <li v-for="loss in props.inform.losses" :key="loss.animal.id">
            <AnimalCard :animal="loss.animal" size="compact" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
