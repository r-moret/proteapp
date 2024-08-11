<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import { useUserStore } from '@/store/UserStore'
import InformEditor from '../components/InformEditor.vue'
import { storeToRefs } from 'pinia'
import type { EditInform } from '@/modules/Inform/declarations'
import { parse, format } from '@formkit/tempo'

const userStore = useUserStore()
const { loggedUser } = storeToRefs(userStore)

const animalStore = useAnimalStore()

const loading = ref(true)
const inform = ref<EditInform>({
  creator: loggedUser.value!.id,
  volunteers: [],
  date: new Date(),
  timeRange: {
    start: format(parse('16:00', 'HH:mm'), 'HH:mm:ssZ'),
    end: format(parse('20:00', 'HH:mm'), 'HH:mm:ssZ')
  },
  notes: [],
  highlights: [],
  visits: [],
  arrivals: [],
  losses: [],
  adoptions: [],
  testedAnimals: []
})

onBeforeMount(async () => {
  await userStore.fetchUsers()
  await animalStore.fetchAnimals()
  loading.value = false
})
</script>

<template>
  <main class="flex flex-col">
    <AppHeader title="Informe" />
    <section class="min-h-0 w-full flex-grow overflow-y-auto px-6">
      <InformEditor v-if="!loading" v-model="inform" />
    </section>
  </main>
</template>
