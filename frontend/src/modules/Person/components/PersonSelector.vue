<script setup lang="ts">
import type { Person } from '@/modules/Person/declarations'
import { ref } from 'vue'
import { usePersonStore } from '@/store/PersonStore'
import { storeToRefs } from 'pinia'
import ItemSelector from '@/components/ItemSelector.vue'
import BottomDrawer from '@/components/BottomDrawer.vue'
import PersonCard from '@/modules/Person/components/PersonCard.vue'

const model = defineModel<Person | null>()

const { personList } = storeToRefs(usePersonStore())

const selectionDrawerOpen = ref(false)
</script>

<template>
  <section class="flex flex-col gap-3">
    <PersonCard v-if="model" :person="model" />
    <button
      class="w-full rounded-xl bg-secondary py-2 font-semibold text-secondary-content"
      @click="selectionDrawerOpen = true"
    >
      Seleccionar persona
    </button>

    <BottomDrawer class="bg-base-200" size="medium" v-model="selectionDrawerOpen">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Selecciona una persona</h1>
        <div class="flex flex-col gap-2">
          <ItemSelector
            :items="personList"
            :model-value="model ? [model] : []"
            :search-fn="(person) => person.name"
            :max-selections="1"
            include-search
            @update:model-value="(selected: Person[]) => (model = selected[0])"
          >
            <template #item="{ item, isSelected, toggleSelect }">
              <PersonCard
                :person="item"
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
  </section>
</template>
