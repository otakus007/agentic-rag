import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getToken, setToken, removeToken, isAuthenticated, logout, login } from '../auth.js'

// Mock localStorage
const localStorageMock = (() => {
  let store = {}
  return {
    getItem: vi.fn((key) => store[key] ?? null),
    setItem: vi.fn((key, value) => { store[key] = value }),
    removeItem: vi.fn((key) => { delete store[key] }),
    clear: vi.fn(() => { store = {} }),
  }
})()

Object.defineProperty(globalThis, 'localStorage', { value: localStorageMock })

beforeEach(() => {
  localStorageMock.clear()
  vi.clearAllMocks()
})

describe('Auth', () => {
  it('getToken returns null when no token', () => {
    expect(getToken()).toBeNull()
  })

  it('setToken stores token in localStorage', () => {
    setToken('my-jwt-token')
    expect(localStorageMock.setItem).toHaveBeenCalledWith('agentic_rag_token', 'my-jwt-token')
  })

  it('getToken returns stored token', () => {
    localStorageMock.getItem.mockReturnValueOnce('my-jwt-token')
    expect(getToken()).toBe('my-jwt-token')
  })

  it('isAuthenticated returns false when no token', () => {
    expect(isAuthenticated()).toBe(false)
  })

  it('isAuthenticated returns true when token exists', () => {
    localStorageMock.getItem.mockReturnValueOnce('some-token')
    expect(isAuthenticated()).toBe(true)
  })

  it('logout removes token', () => {
    logout()
    expect(localStorageMock.removeItem).toHaveBeenCalledWith('agentic_rag_token')
  })

  it('login stores token', () => {
    login('new-token')
    expect(localStorageMock.setItem).toHaveBeenCalledWith('agentic_rag_token', 'new-token')
  })
})
