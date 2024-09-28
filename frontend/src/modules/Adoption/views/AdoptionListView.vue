<script setup lang="ts">
import AppHeader from '@/skeleton/AppHeader.vue'
import AdoptionList from '@/modules/Adoption/components/AdoptionList.vue'
import { useAdoptionStore } from '@/store/AdoptionStore'
import { storeToRefs } from 'pinia'
import { onBeforeMount, ref } from 'vue'
import type { AnimalInfo } from '@/modules/Animal/declarations'
import type { Person } from '@/modules/Person/declarations'
import { EditAdoptionAdapter } from '@/modules/Adoption/adapters'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { ZodError } from 'zod'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { addDay } from '@formkit/tempo'
import BottomDrawer from '@/components/BottomDrawer.vue'
import AnimalSelector from '@/modules/Inform/components/AnimalSelector.vue'
import PersonSelector from '../components/PersonSelector.vue'
import DropdownSelector from '@/components/DropdownSelector.vue'
import { usePersonStore } from '@/store/PersonStore'
import DateInput from '@/components/DateInput.vue'
import type { EditAdoption } from '../declarations'
import { useAnimalStore } from '@/store/AnimalStore'

const notificationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification, showSuccessNotification } = useToastNotifications(notificationsRef)

const personStore = usePersonStore()
const adoptionStore = useAdoptionStore()
const animalStore = useAnimalStore()
const newAdoptionAnimal = ref<AnimalInfo>()
const newAdoptionPerson = ref<Person>()

const newAdoption = ref<EditAdoption>({
  animal: '',
  foster: false,
  person: '',
  registerDate: addDay(new Date())
})
const { adoptionList } = storeToRefs(adoptionStore)

const newAdoptionOpen = ref(false)

async function handleAddAdoption(closeDrawer: () => void) {
  if (!newAdoption.value || !newAdoptionAnimal.value || !newAdoptionPerson.value) return

  try {
    newAdoption.value.registerDate = new Date(
      newAdoption.value.registerDate.getFullYear(),
      newAdoption.value.registerDate.getMonth(),
      newAdoption.value.registerDate.getDate()
    )
    newAdoption.value.animal = newAdoptionAnimal.value.id
    newAdoption.value.person = newAdoptionPerson.value.id

    EditAdoptionAdapter(newAdoption.value)

    await adoptionStore.createAdoption(newAdoption.value)
    showSuccessNotification('Adopción añadida correctamente.')

    newAdoption.value = {
      registerDate: addDay(new Date()),
      foster: false,
      animal: '',
      person: ''
    }
    newAdoptionAnimal.value = undefined
    newAdoptionPerson.value = undefined
    closeDrawer()
  } catch (error) {
    if (error instanceof ZodError) {
      showErrorNotification('Parece que hay un error con los datos de la adopción.')
    } else {
      showErrorNotification('Ha ocurrido un error, prueba otra vez.')
    }
  }
}

onBeforeMount(async () => {
  await personStore.fetchPeople()
  await animalStore.fetchAnimals()
  await adoptionStore.fetchAdoptions()
  newAdoption.value = {
    person: '',
    animal: '',
    registerDate: addDay(new Date()),
    foster: false
  }
  newAdoptionAnimal.value = undefined
  newAdoptionPerson.value = undefined
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificationsRef" />
    <AppHeader left="back" title="Adopciones">
      <button class="btn btn-square btn-ghost" @click="newAdoptionOpen = true">
        <span class="i-mingcute-add-fill text-3xl" />
      </button>
    </AppHeader>

    <section class="min-h-0 w-full flex-grow overflow-y-auto px-4 pt-2">
      <AdoptionList :adoption-list="adoptionList"></AdoptionList>
    </section>

    <BottomDrawer class="bg-base-200" size="big" v-model="newAdoptionOpen" v-slot="{ close }">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Nueva adopción</h1>
        <div v-if="newAdoption" class="flex h-full flex-col gap-6 pb-10">
          <div class="flex flex-col gap-2">
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Animal</h2>
              <AnimalSelector v-model="newAdoptionAnimal" />
            </section>
          </div>
          <div class="flex flex-col gap-2">
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Persona</h2>
              <PersonSelector v-model="newAdoptionPerson" />
            </section>
          </div>

          <div class="flex flex-col gap-2">
            <label class="font-semibold" for="">Fecha de adopción</label>
            <DateInput
              :include-time="false"
              placeholder="ej. 23 de mayo de 2023"
              v-model="newAdoption.registerDate"
            />
          </div>
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
                  type="button"
                  class="flex w-full items-center justify-center gap-2 rounded-xl bg-secondary-content px-4 py-2 font-semibold text-neutral"
                >
                  {{ newAdoption.foster ? 'Casa de acogida' : 'Permanente' }}
                  <span class="i-mingcute-down-fill text-xl" />
                </button>
              </template>
            </DropdownSelector>
          </section>
          <button
            @click="handleAddAdoption(close)"
            class="w-fit self-center rounded-lg bg-secondary px-10 py-3 text-xl font-semibold text-white"
          >
            Añadir
          </button>
        </div>
      </div>
    </BottomDrawer>
  </main>
</template>
