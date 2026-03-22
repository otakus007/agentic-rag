import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'

// We test the router config logic, not the full component tree
vi.mock('../../api/auth.js', () => ({
  isAuthenticated: vi.fn(() => false),
  getToken: vi.fn(() => null),
  logout: vi.fn(),
}))

import { isAuthenticated } from '../../api/auth.js'

async function createTestRouter() {
  const { default: routerConfig } = await import('../index.js')
  // Re-create with memory history for testing
  const router = createRouter({
    history: createMemoryHistory(),
    routes: routerConfig.options.routes,
  })

  router.beforeEach((to) => {
    const needsAuth = to.meta.requiresAuth !== false
    if (needsAuth && !isAuthenticated()) {
      return { name: 'Login', query: { redirect: to.fullPath } }
    }
    if (to.name === 'Login' && isAuthenticated()) {
      return { name: 'Chat' }
    }
  })

  return router
}

describe('Router', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('redirects unauthenticated users to /login', async () => {
    isAuthenticated.mockReturnValue(false)
    const router = await createTestRouter()
    await router.push('/chat')
    expect(router.currentRoute.value.name).toBe('Login')
  })

  it('allows authenticated users to access /chat', async () => {
    isAuthenticated.mockReturnValue(true)
    const router = await createTestRouter()
    await router.push('/chat')
    expect(router.currentRoute.value.name).toBe('Chat')
  })

  it('redirects authenticated users away from /login', async () => {
    isAuthenticated.mockReturnValue(true)
    const router = await createTestRouter()
    await router.push('/login')
    expect(router.currentRoute.value.name).toBe('Chat')
  })

  it('redirects / to /chat', async () => {
    isAuthenticated.mockReturnValue(true)
    const router = await createTestRouter()
    await router.push('/')
    expect(router.currentRoute.value.name).toBe('Chat')
  })
})
