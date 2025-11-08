import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

import DiagnosisSearchView from '@/views/DiagnosisSearchView.vue'
import ConsultationNoteView from '@/views/ConsultationNoteView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ConsultationListView from '@/views/ConsultationListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'search', component: DiagnosisSearchView },
    {
      path: '/consultations/post',
      name: 'consultation-post',
      component: ConsultationNoteView,
      meta: { requiresAuth: true },
    },
    {
      path: '/consultations',
      name: 'consultations',
      component: ConsultationListView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true },
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      meta: { guestOnly: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const guestOnly = to.matched.some(record => record.meta.guestOnly)

  if (requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'login' })
  } else if (guestOnly && authStore.isLoggedIn) {
    next({ name: 'consultations' })
  } else {
    next()
  }
})

export { router }