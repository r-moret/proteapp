import { toValue, type MaybeRef, computed } from 'vue'
import type { Filters } from '@/types'

export const useFilters = <T extends Record<string, any>>(
  elements: MaybeRef<T[]>,
  filters: MaybeRef<Filters>
) => {
  return computed(() => {
    let filtered = toValue(elements)

    for (const filterable in toValue(filters)) {
      const filter = toValue(filters)[filterable]

      filtered = filtered.filter((element) => {
        if (filter.type == 'text') {
          const property = element[filterable] as string
          return property.includes(filter.item)
        } else if (filter.type == 'content') {
          return filter.item.includes(element[filterable])
        }
      })
    }

    return filtered
  })
}
