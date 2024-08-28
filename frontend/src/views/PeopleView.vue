<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import AppHeader from '@/skeleton/AppHeader.vue'
import TabSelector from '@/components/TabSelector.vue'

const Tabs = {
  Registered: {
    label: 'Inscritos',
    route: 'people',
    createRoute: 'people.create',
    editRoute: 'people.edit'
  },
  Volunteers: {
    label: 'Voluntarios',
    route: 'people.volunteers',
    createRoute: 'people.volunteers.create',
    editRoute: 'people.volunteers.edit'
  }
}

const router = useRouter()
const route = useRoute()

const tab = computed(() =>
  Object.values(Tabs).find(
    (tab) =>
      tab.route === route.name || tab.createRoute === route.name || tab.editRoute === route.name
  )
)

function handleSelectTab(newTab: (typeof Tabs)[keyof typeof Tabs]['label']) {
  const tab = Object.values(Tabs).find((tab) => tab.label === newTab)

  router.push({ name: tab?.route })
}

function handleAddClick() {
  router.push({ name: tab.value?.createRoute })
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
        :model-value="tab?.label"
        :tabs="Object.values(Tabs).map((tab) => tab.label)"
        @update:model-value="handleSelectTab"
      />

      <RouterView />
    </section>
  </main>
</template>
