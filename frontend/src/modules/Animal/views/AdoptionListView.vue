<script setup lang="ts">
import AppHeader from '@/skeleton/AppHeader.vue'
import ItemList from '@/components/ItemList.vue'
import { useAdoptionStore } from '@/store/AdoptionStore'
import { storeToRefs } from 'pinia'
import { onBeforeMount } from 'vue'

const adoptionStore = useAdoptionStore()
const { adoptionList } = storeToRefs(adoptionStore)

onBeforeMount(async () => {
  await adoptionStore.fetchAdoptions()
})
</script>

<template>
  <main class="flex flex-col">
    <AppHeader left="back" title="Adopciones" />

    <div class="flex h-3/4 w-full flex-col">
      <ItemList
        :items="adoptionList"
        title="animal"
        :labels="{
          kind: 'Tipo'
        }"
      >
      </ItemList>
    </div>
  </main>
</template>
