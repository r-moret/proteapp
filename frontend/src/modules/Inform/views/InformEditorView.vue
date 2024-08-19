<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import { useUserStore } from '@/store/UserStore'
import { storeToRefs } from 'pinia'
import { useAnimalStore } from '@/store/AnimalStore'
import { useInformStore } from '@/store/InformStore'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { ZodError } from 'zod'
import { useRouter } from 'vue-router'
import { EditInformAdapter } from '@/modules/Inform/adapters'
import InformEditor from '../components/InformEditor.vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import ToastNotifications from '@/components/ToastNotifications.vue'
import type { EditInform } from '@/modules/Inform/declarations'
import { parse, format } from '@formkit/tempo'

const userStore = useUserStore()
const animalStore = useAnimalStore()
const informStore = useInformStore()

const { loggedUser } = storeToRefs(userStore)

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)
const router = useRouter()

const loading = ref(true)
const newInform = ref<EditInform>({
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

async function handleSaveInform() {
  try {
    EditInformAdapter(newInform.value)

    await informStore.createInform(newInform.value)
    showSuccessNotification('Informe añadido correctamente')

    router.push({ name: 'inform' })
  } catch (error) {
    if (error instanceof ZodError) {
      showErrorNotification('Parece que hay un error con los datos del informe.')
    } else {
      showErrorNotification('Ha ocurrido un error, prueba otra vez.')
    }
  }
}

onBeforeMount(async () => {
  await userStore.fetchUsers()
  await animalStore.fetchAnimals()
  loading.value = false
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificationsRef" />

    <AppHeader title="Nuevo informe" left="back">
      <button class="btn btn-square btn-ghost">
        <span class="i-mingcute-save-2-line text-3xl" @click="handleSaveInform" />
      </button>
    </AppHeader>
    <section class="min-h-0 w-full flex-grow overflow-y-auto px-6">
      <InformEditor v-if="!loading" v-model="newInform" />
    </section>
  </main>
</template>
