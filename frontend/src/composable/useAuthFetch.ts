import { useAuthStore } from '@/store/AuthStore'
import { storeToRefs } from 'pinia'

const { token } = storeToRefs(useAuthStore())

export async function authFetch(input: RequestInfo | URL, init: RequestInit = {}) {
  return fetch(input, {
    ...init,
    headers: { ...init.headers, Authorization: `Bearer ${token.value}` }
  })
}
