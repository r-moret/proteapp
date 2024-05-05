<script setup lang="ts">
import type { User } from '@/types'
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    user: User
    size?: 'normal' | 'large'
    ring?: boolean
  }>(),
  {
    size: 'normal',
    ring: false
  }
)

const imageSrc = computed(() => {
  const placeholder_url = `https://ui-avatars.com/api/?background=D6D6D6&color=1C1C1C&size=256&name=${props.user.name}+${props.user.surnames}`
  return props.user.avatar || placeholder_url
})
</script>

<template>
  <div class="avatar">
    <div
      :class="[
        'rounded-full',
        props.size == 'large' ? 'w-28' : 'w-10',
        { 'ring-4 ring-secondary ring-offset-2 ring-offset-base-300': props.ring }
      ]"
    >
      <img alt="User account avatar" :src="imageSrc" />
    </div>
  </div>
</template>
