import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/animals',
      name: 'animals',
      component: () => import('../views/AnimalListView.vue')
    },
    {
      path: '/animals/:id',
      name: 'animal',
      component: () => import('../views/AnimalView.vue')
    },
    {
      path: '/shift',
      name: 'shift',
      component: () => import('../views/ShiftView.vue')
    },
    {
      path: '/inform',
      name: 'inform',
      component: () => import('../views/InformView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue')
    }
  ]
})

export default router
