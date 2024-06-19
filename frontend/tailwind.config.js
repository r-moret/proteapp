/** @type {import('tailwindcss').Config} */

import daisyui from 'daisyui'
import { iconsPlugin, getIconCollections } from '@egoist/tailwindcss-icons'

export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {}
  },
  plugins: [
    daisyui,
    iconsPlugin({
      collections: getIconCollections(['mingcute'])
    })
  ],
  daisyui: {
    themes: ['emerald']
  }
}
