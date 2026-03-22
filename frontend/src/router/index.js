import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '../api/auth.js'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('../views/ChatView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin',
    redirect: '/admin/kb',
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/kb',
    name: 'AdminKB',
    component: () => import('../views/admin/KBListView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/chatbots',
    name: 'AdminChatbots',
    component: () => import('../views/admin/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/',
    redirect: '/chat',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guards
router.beforeEach((to) => {
  const needsAuth = to.meta.requiresAuth !== false

  if (needsAuth && !isAuthenticated()) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  if (to.name === 'Login' && isAuthenticated()) {
    return { name: 'Chat' }
  }
})

export default router
