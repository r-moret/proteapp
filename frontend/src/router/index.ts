import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/people',
      component: () => import('@/views/PeopleView.vue'),
      children: [
        {
          path: '',
          name: 'people',
          component: () => import('@/modules/Person/views/PeopleListSubview.vue')
        },
        {
          path: 'create',
          name: 'people.create',
          component: () => import('@/modules/Person/views/PeopleListSubview.vue')
        },
        {
          path: 'volunteers',
          name: 'people.volunteers',
          component: () => import('@/modules/User/views/UserListSubview.vue')
        }
      ]
    },
    {
      path: '/people/volunteers/create',
      name: 'people.volunteers.create',
      component: () => import('@/modules/User/views/UserEditorView.vue')
    },
    {
      path: '/people/volunteers/:id/edit',
      name: 'people.volunteers.edit',
      component: () => import('@/modules/User/views/UserEditorView.vue')
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
      path: '/animals/create',
      name: 'animal.create',
      component: () => import('@/modules/Animal/views/AnimalEditorView.vue')
    },
    {
      path: '/animals/:id/edit',
      name: 'animal.edit',
      component: () => import('@/modules/Animal/views/AnimalEditorView.vue')
    },
    {
      path: '/yards',
      name: 'yards',
      component: () => import('@/modules/Yard/views/YardsListView.vue')
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
      component: () => import('@/modules/Shift/views/ShiftView.vue')
    },
    {
      path: '/inform',
      name: 'inform',
      component: () => import('@/modules/Inform/views/InformListView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue')
    },
    {
      path: '/inform/edit',
      name: 'inform.edit',
      component: () => import('@/modules/Inform/views/InformEditorView.vue')
    },
    {
      path: '/inform/:id',
      name: 'inform.view',
      component: () => import('@/modules/Inform/views/InformViewerView.vue')
    }
  ]
})

export default router
