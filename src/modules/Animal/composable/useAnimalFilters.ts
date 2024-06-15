import { computed, type Ref } from 'vue'

import type { Animal, AnimalFilters } from '@/types'

export const useAnimalFilters = (animals: Ref<Animal[]>, filters: Ref<AnimalFilters>) => {
  return computed(() => {
    console.log('Reejecuto filtrado')
    let filtered = animals.value

    for (const filterName in filters.value) {
      switch (filterName) {
        case 'name':
          filtered = filtered.filter((animal) => animal.name.includes(filters.value.name))
          break
        case 'yards':
          filtered = filtered.filter((animal) => filters.value.yards[animal.yard])
          break
      }
    }
    return filtered
  })
}
