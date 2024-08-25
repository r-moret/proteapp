<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import AppHeader from '@/skeleton/AppHeader.vue'
import TabSelector from '@/components/TabSelector.vue'

const router = useRouter()

const tab = ref('Todos')

function handleSelectTab(newTab: string) {
  tab.value = newTab
  const newRoute = newTab === 'Voluntarios' ? 'people.volunteers' : 'people'

  router.push({ name: newRoute })
}

function handleAddClick() {
  const newRoute = tab.value === 'Voluntarios' ? 'people.volunteers.create' : 'people.create'
  router.push({ name: newRoute })
}
</script>

<template>
  <main class="flex flex-col">
    <AppHeader left="profile" title="Personas">
      <button class="btn btn-square btn-ghost" @click="handleAddClick">
        <span class="i-mingcute-add-fill text-3xl" />
      </button>
    </AppHeader>

    <section class="min-h-0 w-full flex-grow overflow-y-auto px-4">
      <TabSelector
        class="mb-3"
        :model-value="tab"
        :tabs="['Todos', 'Voluntarios']"
        @update:model-value="handleSelectTab"
      />

      <RouterView />
    </section>
  </main>
</template>
