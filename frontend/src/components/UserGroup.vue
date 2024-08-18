<script setup lang="ts">
import { computed } from 'vue'

import ProfileAvatar from './ProfileAvatar.vue'

import type { UserInfo } from '@/modules/Inform/declarations'

const props = defineProps<{
  users: UserInfo[]
  max?: number
}>()

const showingUsers = computed(() => props.users.slice(0, props.max))
const remainingUsers = computed(() =>
  props.max !== undefined ? props.users.slice(props.max, props.users.length) : ([] as UserInfo[])
)
</script>

<template>
  <div class="avatar-group -space-x-4 rtl:space-x-reverse">
    <ProfileAvatar v-for="user in showingUsers" :user :key="user.id" size="tiny" />
    <div v-if="remainingUsers.length > 0" class="avatar placeholder border-transparent">
      <slot name="remaining" :count="remainingUsers.length">
        <div class="w-8 bg-secondary font-semibold text-white">
          <span>+{{ remainingUsers.length }}</span>
        </div>
      </slot>
    </div>
  </div>
</template>
