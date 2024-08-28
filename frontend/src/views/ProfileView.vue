<script setup lang="ts">
import { onBeforeMount } from 'vue'
import { useAuthStore } from '@/store/AuthStore'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

const router = useRouter()
const { loggedUser } = storeToRefs(useAuthStore())

onBeforeMount(() => {
  router.replace({ name: 'people.volunteers.edit', params: { id: loggedUser.value!.id } })
})
</script>
