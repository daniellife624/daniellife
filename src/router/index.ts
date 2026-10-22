import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { trackVisit } from '@/api/visits'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/activities',
      name: 'activities',
      component: () => import('@/views/ActivitiesView.vue'),
    },
    {
      path: '/social',
      name: 'social',
      component: () => import('@/views/SocialView.vue'),
    },
    {
      path: '/literature',
      name: 'literature',
      component: () => import('@/views/LiteratureView.vue'),
    },
    {
      path: '/market',
      name: 'market',
      component: () => import('@/views/MarketView.vue'),
    },
    {
      path: '/news',
      name: 'news',
      component: () => import('@/views/NewsView.vue'),
    },
    // Admin only
    {
      path: '/thesis',
      name: 'thesis',
      component: () => import('@/views/ThesisView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/finance',
      name: 'finance',
      component: () => import('@/views/FinanceView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/visitors',
      name: 'visitors',
      component: () => import('@/views/VisitorsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/AdminView.vue'),
      meta: { requiresAuth: true },
    },
    // 隱藏登入路由
    {
      path: '/danieladmin',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    // 403
    {
      path: '/403',
      name: 'forbidden',
      component: () => import('@/views/ForbiddenView.vue'),
    },
    // 404
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/',
    },
  ],
})

// 權限守衛
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { name: 'forbidden' }
  }
})

// 訪客記錄：只記公開頁面，登入狀態不記
const UNTRACKED = new Set(['login', 'forbidden'])
router.afterEach((to, from, failure) => {
  if (failure || to.meta.requiresAuth || UNTRACKED.has(String(to.name))) return
  if (useAuthStore().isLoggedIn) return
  const src = typeof to.query.src === 'string' ? to.query.src : ''
  trackVisit(to.path, src)
})

export default router