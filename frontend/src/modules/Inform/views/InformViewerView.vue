<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import { storeToRefs } from 'pinia'

import { useParams } from '@/composable/useParams'
import { useInformStore } from '@/store/InformStore'
import { useUserStore } from '@/store/UserStore'
import { useAnimalStore } from '@/store/AnimalStore'
import { toLocal } from '@/utils'

import InformViewer from '@/modules/Inform/components/InformViewer.vue'
import AppHeader from '@/skeleton/AppHeader.vue'

import type { EnrichedInform, Inform } from '@/modules/Inform/declarations'

const routeParams = useParams<{ id: string }>()

const animalStore = useAnimalStore()
const userStore = useUserStore()
const informStore = useInformStore()

const { informDetails } = storeToRefs(informStore)
const { userList } = storeToRefs(userStore)
const { animalList } = storeToRefs(animalStore)

const isLoading = ref(false)
const enrichedInform = ref<EnrichedInform>()

function enrichInform(inform: Inform): EnrichedInform {
  return {
    creator: userList.value.find((user) => user.id === inform!.creator.id)!, // TODO
    volunteers: inform.volunteers.map(
      (vol) => userList.value.find((user) => user.id === vol.id)! // TODO
    ),
    date: inform.date,
    timeRange: [
      {
        hours: toLocal(inform.timeRange.start).getHours(),
        minutes: toLocal(inform.timeRange.start).getMinutes()
      },
      {
        hours: toLocal(inform.timeRange.end).getHours(),
        minutes: toLocal(inform.timeRange.end).getMinutes()
      }
    ],
    highlights: inform.highlights,
    notes: inform.notes?.map((note) => ({
      info: animalList.value.find((animal) => animal.id === note.animal.id)!, // TODO
      note: note.text
    })),
    adoptions: inform.adoptions?.map((adop) => ({
      animal: animalList.value.find((animal) => animal.id === adop.animal.id)!, // TODO
      foster: adop.foster
    })),
    testedAnimals: inform.testedAnimals?.map((test) => ({
      animal: animalList.value.find((animal) => animal.id === test.animal.id)!, // TODO
      compatible: test.compatible
    })),
    losses: inform.losses?.map((loss) => ({
      animal: animalList.value.find((animal) => animal.id === loss.animal.id)! // TODO
    })),
    visits: inform.visits,
    arrivals: inform.arrivals
  }
}

onBeforeMount(async () => {
  isLoading.value = true

  await informStore.fetchInform(routeParams.value.id)
  await animalStore.fetchAnimals()
  await userStore.fetchUsers()

  if (!(informDetails.value && userList.value && animalList.value)) return

  enrichedInform.value = enrichInform(informDetails.value)

  isLoading.value = false
})
</script>

<template>
  <main class="flex flex-col">
    <AppHeader title="Informe" left="back" />
    <section
      v-if="isLoading || !enrichedInform"
      class="flex h-full w-full items-center justify-center"
    >
      <span class="loading loading-spinner loading-lg text-secondary" />
    </section>
    <section v-else class="min-h-0 w-full flex-grow overflow-y-auto px-6">
      <InformViewer :inform="enrichedInform" />
    </section>
  </main>
</template>
