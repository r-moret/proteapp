<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import { useParams } from '@/composable/useParams'
import TextInput from '@/components/TextInput.vue'
import ImagePicker from '@/components/ImagePicker.vue'
import DateInput from '@/components/DateInput.vue'
import type { EnrichedEditAnimal } from '@/modules/Animal/declarations'
import { EnrichedEditAnimalAdapter } from '@/modules/Animal/adapters'
import { useAnimalStore } from '@/store/AnimalStore'
import YardSelector from '@/modules/Animal/components/YardSelector.vue'
import ToastNotifications from '@/components/ToastNotifications.vue'
import { useToastNotifications } from '@/composable/useToastNotifications'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

const params = useParams<{
  id?: string
}>()

const animalStore = useAnimalStore()
const { animalDetails } = storeToRefs(animalStore)

const router = useRouter()

const notificiationsRef = ref<InstanceType<typeof ToastNotifications> | null>(null)
const { showErrorNotification } = useToastNotifications(notificiationsRef)

const isEditMode = ref(!!params.value.id)
const editingAnimal = ref<Partial<EnrichedEditAnimal>>()

function handleSexInput(sex: EnrichedEditAnimal['sex']) {
  if (!editingAnimal.value) return
  editingAnimal.value.sex = sex
}

async function handleSaveAnimal() {
  try {
    EnrichedEditAnimalAdapter(editingAnimal.value)
  } catch (error) {
    showErrorNotification(
      'Faltan datos para poder guardar el animal o están en un formato incorrecto.'
    )
    return
  }

  try {
    if (isEditMode.value && params.value.id) {
      await animalStore.updateAnimal(params.value.id, editingAnimal.value as EnrichedEditAnimal)
    } else {
      await animalStore.createAnimal(editingAnimal.value as EnrichedEditAnimal)
    }

    router.push({ name: 'animals' })
  } catch (error) {
    showErrorNotification(
      'Parece que un error inesperado ocurrió guardando el animal, por favor prueba de nuevo.'
    )
    return
  }
}

onBeforeMount(async () => {
  if (isEditMode.value) {
    await animalStore.fetchAnimal(params.value.id!)

    if (!animalDetails.value) {
      showErrorNotification('No se encontró ningún animal.')
      router.push({ name: 'animals' })
      return
    }

    editingAnimal.value = {
      ...animalDetails.value
    }
  } else {
    editingAnimal.value = {
      name: undefined,
      sex: undefined,
      birthDate: undefined,
      entryDate: undefined,
      isCastrated: false,
      isAnimalCompatible: false,
      description: undefined,
      personality: undefined,
      image: undefined,
      yard: undefined
    }
  }
})
</script>

<template>
  <main class="flex flex-col">
    <ToastNotifications ref="notificiationsRef" />

    <AppHeader left="back" :title="isEditMode ? 'Editar animal' : 'Crear animal'">
      <button class="btn btn-square btn-ghost" @click="handleSaveAnimal">
        <span class="i-mingcute-save-2-line text-3xl" />
      </button>
    </AppHeader>

    <section class="min-h-0 w-full flex-grow overflow-y-auto px-6 pb-8">
      <div v-if="editingAnimal" class="flex flex-col gap-4">
        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Nombre</h2>
          <TextInput placeholder="Nombre del animal" v-model="editingAnimal.name">
            <template #icon>
              <span class="i-mingcute-cat-fill text-2xl text-secondary" />
            </template>
          </TextInput>
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Imagen</h2>
          <ImagePicker v-model="editingAnimal.image" class="px-2" />
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Sexo</h2>
          <div class="flex gap-4">
            <label class="label cursor-pointer gap-2">
              <input
                type="radio"
                name="radio-sex"
                class="radio-secondary radio"
                :checked="editingAnimal.sex === 'male'"
                @change="handleSexInput('male')"
              />
              <span class="label-text font-semibold">Masculino</span>
            </label>
            <label class="label cursor-pointer gap-2">
              <input
                type="radio"
                name="radio-sex"
                class="radio-secondary radio"
                :checked="editingAnimal.sex === 'female'"
                @change="handleSexInput('female')"
              />
              <span class="label-text font-semibold">Femenino</span>
            </label>
          </div>
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Fecha de nacimiento</h2>
          <DateInput
            v-model="editingAnimal.birthDate"
            :include-time="false"
            placeholder="Nacimiento (aproximado) del animal"
          />
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Fecha de entrada</h2>
          <DateInput
            v-model="editingAnimal.entryDate"
            :include-time="false"
            placeholder="Día que se registró en la protectora"
          />
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Patio</h2>
          <YardSelector v-model="editingAnimal.yard" />
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Personalidad</h2>
          <textarea
            v-model="editingAnimal.personality"
            class="rounded-lg p-4"
            rows="2"
            placeholder="Una pequeña frase que resuma su comportamiento"
          />
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Detalles</h2>
          <div class="flex flex-col gap-1">
            <label class="label gap-2">
              <input
                type="checkbox"
                class="checkbox-secondary checkbox"
                v-model="editingAnimal.isAnimalCompatible"
              />
              <span class="label-text w-full text-start font-semibold">
                Compatible con otros animales
              </span>
            </label>
            <label class="label gap-2">
              <input
                type="checkbox"
                class="checkbox-secondary checkbox"
                v-model="editingAnimal.isCastrated"
              />
              <span class="label-text w-full text-start font-semibold"> Castrado </span>
            </label>
          </div>
        </div>

        <div class="flex flex-col gap-2">
          <h2 class="text-xl font-semibold">Descripción</h2>
          <textarea
            v-model="editingAnimal.description"
            class="rounded-lg p-4"
            rows="6"
            placeholder="De dónde viene, cómo es, quiénes fueron sus anteriores dueños..."
          />
        </div>
      </div>
    </section>
  </main>
</template>
