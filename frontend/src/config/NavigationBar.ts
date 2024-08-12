import type { NavigationBarConfig } from '@/types.ts'

export const navigationBarConfig: NavigationBarConfig = {
  items: [
    {
      name: 'people',
      label: 'Personas',
      icon: 'i-mingcute-user-2-fill',
      activeIcon: 'i-mingcute-user-2-fill'
    },
    {
      name: 'animals',
      label: 'Animales',
      icon: 'i-mingcute-cat-line',
      activeIcon: 'i-mingcute-cat-fill'
    },
    {
      name: 'shift',
      label: 'Cuadrante',
      icon: 'i-mingcute-group-3-line',
      activeIcon: 'i-mingcute-group-3-fill'
    },
    {
      name: 'inform',
      label: 'Informe',
      icon: 'i-mingcute-pencil-line',
      activeIcon: 'i-mingcute-pencil-fill'
    }
  ]
}
