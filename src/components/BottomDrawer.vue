<script setup lang="ts">
import { ref } from 'vue'

defineOptions({
  inheritAttrs: false
})

const props = withDefaults(
  defineProps<{
    includeClose: boolean
  }>(),
  {
    includeClose: true
  }
)

const isOpen = ref(false)
const isClosing = ref(false)

const handleCloseSlide = () => {
  if (!isClosing.value) return

  isClosing.value = false
  isOpen.value = false
}
</script>

<template>
  <slot name="button" :open="() => (isOpen = true)" />

  <Teleport to="body">
    <div v-show="isOpen" class="fixed top-0 grid h-screen w-screen">
      <span class="col-start-1 row-start-1 bg-black bg-opacity-60" @click="isClosing = true" />
      <div
        v-bind="$attrs"
        @animationend="handleCloseSlide"
        :class="[
          'col-start-1 row-start-1 flex h-3/4 w-full flex-col place-self-end rounded-t-3xl p-4',
          isClosing ? 'slide-out' : 'slide-in'
        ]"
      >
        <button
          v-if="props.includeClose"
          class="flex items-center justify-end"
          @click="isClosing = true"
        >
          <span class="i-mingcute-close-line text-2xl" />
        </button>
        <div class="flex-1">
          <slot name="drawer" :close="() => (isClosing = true)" />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.slide-in {
  animation: slide-in 0.3s forwards;
}

.slide-out {
  animation: slide-out 0.3s forwards;
}

@keyframes slide-in {
  0% {
    transform: translateY(100%);
  }

  100% {
    transform: translateY(0%);
  }
}

@keyframes slide-out {
  0% {
    transform: translateY(0%);
  }

  100% {
    transform: translateY(100%);
  }
}
</style>
