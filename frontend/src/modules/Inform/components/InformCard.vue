<script setup lang="ts">
import { computed } from 'vue'
import type { InformInfo } from '../declarations'
import { format, isAfter, parse } from '@formkit/tempo'
import { shiftType } from '@/utils'

const props = defineProps<{
  inform: InformInfo
}>()

const volunteersNames = computed(() => {
  const fullName = (...names: (string | undefined | null)[]) =>
    names.reduce((full, name) => (name ? full + ` ${name}` : full), '')

  const creator = fullName(
    props.inform.creator.person.name,
    props.inform.creator.person.firstSurname,
    props.inform.creator.person.secondSurname
  )

  return [
    creator,
    ...props.inform.volunteers.map((vol) =>
      fullName(vol.person.name, vol.person.firstSurname, vol.person.secondSurname)
    )
  ].join(', ')
})

const shift = computed(() => shiftType(parse(props.inform.timeRange.start, 'HH:mm:ssZ')))

const formatedTime = computed(
  () => `${formatTime(props.inform.timeRange.start)} - ${formatTime(props.inform.timeRange.end)}`
)

function formatTime(time: string) {
  return format(parse(time, 'HH:mm:ssZ'), { time: 'short' })
}
</script>

<template>
  <article
    class="flex flex-col items-start gap-2 rounded-2xl bg-secondary-content px-4 py-4 shadow-sm"
  >
    <div class="flex w-full items-center justify-between">
      <header class="flex items-center gap-2">
        <h1 class="text-lg font-semibold text-secondary first-letter:uppercase">
          {{ format(props.inform.date, { date: 'full' }) }}
        </h1>
        <p class="italic">({{ shift }})</p>
      </header>
      <div v-if="$slots.action">
        <slot name="action" />
      </div>
    </div>
    <section class="flex w-full flex-wrap items-center gap-x-6">
      <div class="flex flex-nowrap items-center gap-2">
        <span class="i-mingcute-group-fill text-lg text-secondary" />
        <p class="text-nowrap">{{ volunteersNames }}</p>
      </div>
      <div class="flex flex-nowrap items-center gap-2">
        <span class="i-mingcute-time-fill text-lg text-secondary" />
        <p class="text-nowrap">{{ formatedTime }}</p>
      </div>
    </section>
  </article>
</template>
