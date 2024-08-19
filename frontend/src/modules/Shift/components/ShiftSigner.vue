<script setup lang="ts">
import { computed } from 'vue'

import UserGroup from '@/components/UserGroup.vue'

import type { UserInfo } from '@/modules/Inform/declarations'

const props = withDefaults(
  defineProps<{
    time: 'morning' | 'afternoon'
    users?: UserInfo[]
    highlight?: boolean
    maxUsers: number
  }>(),
  {
    users: () => []
  }
)

const emit = defineEmits<{
  select: []
}>()

const isVeteranMissing = computed(
  () => props.users.length > 0 && !props.users.some((user) => user.veteran)
)
const isCompleted = computed(() => props.users.length >= props.maxUsers && !isVeteranMissing.value)

function handleClick() {
  if (isCompleted.value && !props.highlight) return

  emit('select')
}
</script>

<template>
  <article
    :class="[
      'flex flex-col items-center justify-between rounded-lg border-2 pb-4 pt-5 shadow-md',
      props.highlight
        ? 'border-secondary bg-white shadow-secondary'
        : isCompleted
          ? 'border-neutral-400 border-opacity-80 bg-neutral-100'
          : 'border-transparent bg-white'
    ]"
    @click="handleClick"
  >
    <div
      :class="[
        'flex items-center justify-center gap-2',
        props.highlight ? 'text-secondary' : isCompleted ? 'text-neutral-400' : 'text-neutral'
      ]"
    >
      <span
        :class="[
          'text-4xl',
          props.time === 'morning' ? 'i-mingcute-sun-line' : 'i-mingcute-sun-fog-line'
        ]"
      />
      <p class="font-semibold">{{ props.time === 'morning' ? 'Mañana' : 'Tarde' }}</p>
    </div>
    <span
      v-if="isCompleted"
      :class="[
        'badge border-2 p-2 py-3 font-semibold uppercase',
        props.highlight
          ? 'border-secondary text-secondary'
          : 'border-neutral border-opacity-50 bg-neutral-100 text-neutral text-opacity-70'
      ]"
    >
      Completo
    </span>
    <span
      v-else-if="isVeteranMissing"
      :class="[
        'badge border-2  p-2 py-3 font-semibold uppercase',
        props.highlight ? 'border-secondary text-secondary' : 'border-neutral text-neutral'
      ]"
    >
      Falta veterano
    </span>
    <p v-if="props.users.length === 0" class="text-center italic text-gray-500">Vacío</p>
    <UserGroup v-else :users="props.users" :max="3">
      <template #remaining="{ count }">
        <div
          :class="[
            'w-8 font-semibold',
            props.highlight
              ? 'bg-secondary text-white'
              : isCompleted
                ? 'bg-neutral-300 text-neutral'
                : 'bg-neutral text-neutral-content'
          ]"
        >
          <span>+{{ count }}</span>
        </div>
      </template>
    </UserGroup>
  </article>
</template>
