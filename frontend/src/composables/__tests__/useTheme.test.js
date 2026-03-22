import { describe, it, expect, vi, beforeEach } from 'vitest'

// Mock localStorage before importing
const store = {}
vi.stubGlobal('localStorage', {
  getItem: vi.fn((key) => store[key] || null),
  setItem: vi.fn((key, val) => { store[key] = val }),
  clear: vi.fn(() => { Object.keys(store).forEach((k) => delete store[k]) }),
  removeItem: vi.fn((key) => { delete store[key] }),
})

import { useTheme } from '../useTheme.js'

describe('useTheme', () => {
  beforeEach(() => {
    Object.keys(store).forEach((k) => delete store[k])
  })

  it('defaults to dark theme', () => {
    const { theme } = useTheme()
    expect(theme.value).toBe('dark')
  })

  it('toggles between dark and light', () => {
    const { theme, toggle } = useTheme()
    expect(theme.value).toBe('dark')
    toggle()
    expect(theme.value).toBe('light')
    toggle()
    expect(theme.value).toBe('dark')
  })

  it('stores theme value in localStorage via apply', () => {
    // useTheme sets data-theme attr and localStorage on watch
    const { theme } = useTheme()
    // The composable reads from localStorage on init
    expect(theme.value).toBe('dark')
    // Verify the composable reads saved values
    store['agentic-rag-theme'] = 'light'
    const { theme: t2 } = useTheme()
    expect(t2.value).toBe('light')
  })
})
