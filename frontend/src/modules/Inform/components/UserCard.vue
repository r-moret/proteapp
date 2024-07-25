<script setup lang="ts">
import { computed } from 'vue'
import type { UserInfo } from '@/modules/Inform/declarations'

const props = defineProps<{
  user: UserInfo
  size: 'compact' | 'regular'
}>()

const placerholderImage = computed(
  () =>
    `https://ui-avatars.com/api/?background=f9fafb&color=333c4d&size=256&name=${props.user.person.name}+${props.user.person.firstSurname}`
)
const fullName = computed(
  () =>
    props.user.person.name +
    ' ' +
    props.user.person.firstSurname +
    (props.user.person.secondSurname ? ' ' + props.user.person.secondSurname : '')
)
</script>

<template>
  <article
    :class="[
      'flex items-center gap-4 rounded-2xl bg-secondary-content px-3 py-2 shadow-sm',
      { grayscale: !props.user.active }
    ]"
  >
    <img
      :class="[
        'rounded-full border-2 border-secondary object-cover shadow-xl',
        props.size === 'compact' ? 'h-12 w-12' : 'h-16 w-16'
      ]"
      :src="props.user.image ?? placerholderImage"
      alt="User profile avatar image"
    />
    <section>
      <header class="flex items-center gap-3">
        <p class="text-lg font-semibold">{{ fullName }}</p>
        <span
          v-if="props.user.veteran && props.size === 'regular'"
          class="i-mingcute-user-star-fill text-2xl text-secondary"
        />
      </header>
      <div v-if="props.size === 'regular'" class="italic">{{ props.user.person.email }}</div>
      <div v-if="!props.user.active" class="badge badge-secondary font-semibold uppercase">
        INACTIVE
      </div>
    </section>
  </article>
</template>
