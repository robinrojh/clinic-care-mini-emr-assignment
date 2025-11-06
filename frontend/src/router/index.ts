import ConsultationNoteView from '@/views/ConsultationNoteView.vue'
import DiagnosisSearchView from '@/views/DiagnosisSearchView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'search',
    component: DiagnosisSearchView
  },
  {
    path: '/consultations',
    name: 'consultations',
    component: ConsultationNoteView
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes: routes
})