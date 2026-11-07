import { createRouter, createWebHistory } from 'vue-router'
import { useSessionStore } from '@/stores/session'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'inicio',
      component: () => import('@/pages/HomePage.vue'),
    },
    {
      path: '/estimar',
      name: 'estimar',
      component: () => import('@/pages/EstimacionPage.vue'),
    },
    {
      path: '/estimaciones/:estimacionId',
      name: 'resultado',
      component: () => import('@/pages/ResultadoPage.vue'),
      props: true,
    },
    {
      path: '/historial',
      name: 'historial',
      component: () => import('@/pages/HistorialPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/componentes',
      name: 'componentes',
      component: () => import('@/pages/ComponentesPage.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/LoginPage.vue'),
      meta: { soloInvitados: true },
    },
    {
      path: '/registro',
      name: 'registro',
      component: () => import('@/pages/RegistroPage.vue'),
      meta: { soloInvitados: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'no-encontrada',
      component: () => import('@/pages/NotFoundPage.vue'),
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const session = useSessionStore()

  if (to.meta.requiresAuth && !session.estaAutenticado) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.soloInvitados && session.estaAutenticado) {
    return { name: 'inicio' }
  }

  return true
})

export default router
