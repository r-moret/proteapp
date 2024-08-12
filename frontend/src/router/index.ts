import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'people',
      component: () => import('@/modules/Person/views/PeopleListView.vue')
    },
    {
      path: '/animals',
      name: 'animals',
      component: () => import('@/modules/Animal/views/AnimalListView.vue')
    },
    {
      path: '/animals/:id',
      name: 'animal',
      component: () => import('@/modules/Animal/views/AnimalView.vue')
    },
    {
      path: '/animals/:id/treatments',
      name: 'animal.treatments',
      component: () => import('@/modules/Animal/views/TreatmentsView.vue')
    },
    {
      path: '/animals/:id/appointments',
      name: 'animal.appointments',
      component: () => import('@/modules/Animal/views/AppointmentsView.vue')
    },
    {
      path: '/adoptions',
      name: 'adoptions',
      component: () => import('@/modules/Adoption/views/AdoptionListView.vue')
    },
    {
      path: '/adoptions/:id',
      name: 'adoption',
      component: () => import('@/modules/Adoption/views/AdoptionView.vue')
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
