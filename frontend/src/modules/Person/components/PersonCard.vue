<script setup lang="ts">
import type { Person } from '@/modules/Person/declarations'

function getFullName(name: String, firstSurname: String, secondSurname: String | null | undefined) {
  return `${name} ${firstSurname}${secondSurname ? ' ' + secondSurname : ''}`
}

function getPhone(phone: String) {
  return phone.substring(3)
}

const props = defineProps<{
  person: Person
}>()
</script>

<template>
  <article
    :class="['flex justify-between gap-4 rounded-2xl bg-secondary-content px-3 py-2 shadow-sm']"
  >
    <section class="px-2 py-1">
      <header class="flex items-center">
        <p class="text-lg font-semibold">
          {{
            getFullName(props.person.name, props.person.firstSurname, props.person.secondSurname)
          }}
        </p>
      </header>
      <span class="italic"> {{ props.person.email }} </span>
      <span> - </span>
      <span class="italic">{{ getPhone(props.person.phone) }}</span>
    </section>
    <div class="self-start">
      <slot name="action" />
    </div>
  </article>
</template>
