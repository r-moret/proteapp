<script setup lang="ts">
import { onBeforeMount, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { format, parse, sameDay } from '@formkit/tempo'

import { useInformStore } from '@/store/InformStore'
import { shiftType } from '@/utils'

import DateInput from '@/components/DateInput.vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import ItemList from '@/components/ItemList.vue'
import InformCard from '@/modules/Inform/components/InformCard.vue'

import type { InformInfo } from '@/modules/Inform/declarations'

const router = useRouter()

const informStore = useInformStore()
const { informList } = storeToRefs(informStore)

const filterDate = ref<Date>()

const filteredInforms = computed(() =>
  filterDate.value
    ? informList.value.filter((inform) => sameDay(inform.date, filterDate.value!))
    : informList.value
)

async function handleDeleteInform(inform: InformInfo) {
  await informStore.deleteInform(inform.id)
}

function handleNewInform() {
  router.push({ name: 'inform.edit' })
}

function handleViewInform(informId: string) {
  router.push({ name: 'inform.view', params: { id: informId } })
}

onBeforeMount(async () => {
  await informStore.fetchInforms()
})
</script>

<template>
  <main class="flex flex-col">
    <AppHeader title="Informe">
      <button class="btn btn-square btn-ghost" @click="handleNewInform">
        <span class="i-mingcute-add-line text-3xl" />
      </button>
    </AppHeader>
    <section class="min-h-0 w-full flex-grow overflow-y-auto px-4">
      <DateInput
        class="mb-6 mt-2"
        v-model="filterDate"
        :include-time="false"
        placeholder="Buscar por fecha"
      />
      <ItemList
        :items="filteredInforms"
        delete-title="¿Estás seguro de que quieres borrar este informe?"
        @delete="handleDeleteInform"
      >
        <template #empty>
          <div class="mt-4 flex flex-col items-center gap-2">
            <span class="i-mingcute-file-unknown-line text-6xl" />
            <p class="text-gray-500">No hay informes</p>
          </div>
        </template>
        <template #item="{ item, openConfirm }">
          <InformCard :inform="item" @click="handleViewInform(item.id)">
            <template #action>
              <button type="button" @click.stop="openConfirm(item)">
                <span class="i-mingcute-close-fill" />
              </button>
            </template>
          </InformCard>
        </template>
        <template #delete="{ item }">
          <p class="first-letter:uppercase">
            <span class="font-semibold">{{ format(item.date, { date: 'full' }) }}</span> (turno de
            {{ shiftType(parse(item.timeRange.start, 'HH:mm:ssZ')) }})
          </p>
        </template>
      </ItemList>
    </section>
  </main>
</template>
