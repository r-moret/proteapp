<script setup lang="ts">
import { computed } from 'vue'

import type { UserInfo } from '@/modules/Inform/declarations'

const SIZES = {
  tiny: 'w-8',
  normal: 'w-10',
  large: 'w-28'
}

const props = withDefaults(
  defineProps<{
    user: UserInfo
    size?: 'tiny' | 'normal' | 'large'
    ring?: boolean
  }>(),
  {
    size: 'normal',
    ring: false
  }
)

const imageSrc = computed(() => {
  const placeholder_url = `https://ui-avatars.com/api/?background=D6D6D6&color=1C1C1C&size=256&name=${props.user.person.name}+${props.user.person.firstSurname}`
  return props.user.image || placeholder_url
})
</script>

<template>
  <div class="avatar border-transparent">
    <div
      :class="[
        'rounded-full',
        SIZES[props.size],
        { 'ring-4 ring-secondary ring-offset-2 ring-offset-base-300': props.ring }
      ]"
    >
      <img alt="User account avatar" :src="imageSrc" />
    </div>
  </div>
</template>
