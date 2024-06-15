import { computed, type Ref } from 'vue'

import type { Animal, AnimalFilters } from '@/types'
import { diffYears } from '@formkit/tempo'

const age = (birthdate: Date) => diffYears(new Date(), birthdate)

export const useAnimalFilters = (animals: Ref<Animal[]>, filters: Ref<AnimalFilters>) => {
  return computed(() => {
    let filtered = animals.value

    for (const filterName in filters.value) {
      switch (filterName) {
        case 'name':
          filtered = filtered.filter((animal) => animal.name.includes(filters.value.name))
          break
        case 'yards':
          filtered = filtered.filter((animal) => filters.value.yards[animal.yard])
          break
        case 'sex':
          filtered = filtered.filter((animal) => filters.value.sex[animal.sex])
          break
        case 'age':
          filtered = filtered.filter(
            (animal) =>
              age(animal.birthDate) <= filters.value.age.max &&
              age(animal.birthDate) >= filters.value.age.min
          )
          break
        case 'castration':
          filtered = filtered.filter(
            (animal) => filters.value.castration[animal.isCastrated ? 'true' : 'false']
          )
          break
        case 'compatible':
          filtered = filtered.filter(
            (animal) => filters.value.compatible[animal.isAnimalCompatible ? 'true' : 'false']
          )
          break
      }
    }
    return filtered
  })
}
