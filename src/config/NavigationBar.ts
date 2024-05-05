import type { NavigationBarConfig } from '@/types.ts'

export const navigationBarConfig: NavigationBarConfig = {
  items: [
    {
      name: 'home',
      label: 'Inicio',
      icon: 'i-mingcute-home-3-line',
      activeIcon: 'i-mingcute-home-3-fill'
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
