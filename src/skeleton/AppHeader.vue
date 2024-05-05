<script setup lang="ts">
import ProfileAvatar from '@/components/ProfileAvatar.vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/store/UserStore'

const props = withDefaults(
  defineProps<{
    left?: 'profile' | 'back'
    title?: string
  }>(),
  {
    left: 'profile',
    title: ''
  }
)

const { user, isLoading } = storeToRefs(useUserStore())

const router = useRouter()

const openProfile = () => router.push('/profile')
const navigateBack = () => router.back()
</script>

<template>
  <div class="navbar h-16 gap-4 px-4">
    <div class="min-w-0 flex-1">
      <template v-if="props.left == 'profile'">
        <ProfileAvatar
          v-if="!isLoading"
          :user="user"
          class="btn btn-circle btn-ghost btn-lg"
          @click="openProfile"
        />
        <div v-else class="avatar btn btn-circle btn-ghost btn-lg" @click="openProfile">
          <div class="skeleton h-10 w-10 rounded-full"></div>
        </div>
      </template>
      <button v-else class="btn btn-square btn-ghost" @click="navigateBack">
        <span class="i-mingcute-left-line text-4xl text-base-content" />
      </button>
      <p
        v-if="props.title"
        class="truncate px-2 align-middle text-xl font-semibold text-base-content"
      >
        {{ props.title }}
      </p>
    </div>
    <div class="flex-none gap-2">
      <slot></slot>
    </div>
  </div>
</template>
