<script setup lang="ts">
import ProfileAvatar from '@/components/ProfileAvatar.vue'
import AppHeader from '@/skeleton/AppHeader.vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/store/UserStore'

const { loggedUser } = storeToRefs(useUserStore())
</script>

<template>
  <main class="flex flex-col items-start gap-6 text-base-content">
    <AppHeader left="back" />
    <div class="flex w-full flex-col gap-10 px-4">
      <div v-if="loggedUser" class="flex w-full items-end gap-8 px-4">
        <ProfileAvatar :user="loggedUser" size="large" :ring="true" />
        <div class="w-full">
          <h2 class="text-2xl font-bold">
            {{ loggedUser.person.name + ' ' + loggedUser.person.firstSurname }}
          </h2>
          <p class="mb-2 text-sm font-semibold">{{ loggedUser.person.email }}</p>
          <div
            :class="[
              { 'badge-outline': !loggedUser.veteran },
              'badge badge-secondary gap-2 px-2 py-3'
            ]"
          >
            <span
              :class="[
                'text-xl',
                loggedUser.veteran ? 'i-mingcute-safe-lock-fill' : 'i-mingcute-shield-shape-line'
              ]"
            />
            <p class="text-sm font-semibold">{{ loggedUser.veteran ? 'Veterano' : 'Novato' }}</p>
          </div>
        </div>
      </div>
      <ul class="menu w-full gap-1 rounded-box">
        <li>
          <a>
            <span class="i-mingcute-tool-line text-3xl" />
            <p class="px-2 text-xl font-semibold">Opción 1</p>
          </a>
        </li>
        <li>
          <a
            ><span class="i-mingcute-calendar-add-line text-3xl" />
            <p class="px-2 text-xl font-semibold">Opción 2</p>
          </a>
        </li>
        <li>
          <a
            ><span class="i-mingcute-user-add-2-line text-3xl" />
            <p class="px-2 text-xl font-semibold">Opción 3</p>
          </a>
        </li>
        <li>
          <a class="hover:text-red-600"
            ><span class="i-mingcute-delete-2-line text-3xl" />
            <p class="px-2 text-xl font-semibold">Dar de baja</p>
          </a>
        </li>
      </ul>
    </div>
  </main>
</template>
