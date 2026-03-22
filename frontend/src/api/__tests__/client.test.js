import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock auth module
vi.mock('../auth.js', () => ({
  getToken: vi.fn(() => 'mock-jwt-token'),
  logout: vi.fn(),
}))

describe('API Client', () => {
  it('module exports an axios instance', async () => {
    const { default: apiClient } = await import('../client.js')
    expect(apiClient).toBeDefined()
    expect(typeof apiClient.get).toBe('function')
    expect(typeof apiClient.post).toBe('function')
  })

  it('has interceptors configured', async () => {
    const { default: apiClient } = await import('../client.js')
    // Axios interceptors managers have a handlers array
    expect(apiClient.interceptors.request.handlers.length).toBeGreaterThan(0)
    expect(apiClient.interceptors.response.handlers.length).toBeGreaterThan(0)
  })
})
