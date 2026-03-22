import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useChat } from '../useChat.js'
import { nextTick } from 'vue'

// Mock the API client
vi.mock('../../api/client.js', () => ({
  default: {
    post: vi.fn(),
  },
}))

import apiClient from '../../api/client.js'

describe('useChat', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('starts with empty state', () => {
    const { messages, isLoading, error } = useChat()
    expect(messages.value).toEqual([])
    expect(isLoading.value).toBe(false)
    expect(error.value).toBeNull()
  })

  it('sends message and appends response', async () => {
    apiClient.post.mockResolvedValueOnce({
      data: {
        answer: 'Hello! Based on [1], yes.',
        sources: [{ content: 'Source text', page_number: 1, block_type: 'paragraph' }],
      },
    })

    const { messages, sendMessage } = useChat()
    await sendMessage('hi', 'agent-1')

    expect(messages.value).toHaveLength(2)
    expect(messages.value[0]).toEqual({ role: 'user', content: 'hi' })
    expect(messages.value[1].role).toBe('assistant')
    expect(messages.value[1].content).toBe('Hello! Based on [1], yes.')
    expect(messages.value[1].sources).toHaveLength(1)
  })

  it('sets isLoading during API call', async () => {
    let resolvePromise
    apiClient.post.mockReturnValueOnce(
      new Promise((resolve) => {
        resolvePromise = resolve
      })
    )

    const { isLoading, sendMessage } = useChat()
    const promise = sendMessage('test', 'agent-1')
    await nextTick()

    expect(isLoading.value).toBe(true)

    resolvePromise({ data: { answer: 'ok', sources: [] } })
    await promise

    expect(isLoading.value).toBe(false)
  })

  it('captures errors without crashing', async () => {
    apiClient.post.mockRejectedValueOnce(new Error('Network error'))

    const { messages, error, sendMessage } = useChat()
    await sendMessage('test', 'agent-1')

    expect(error.value).toBe('Network error')
    expect(messages.value).toHaveLength(2)
    expect(messages.value[1].role).toBe('assistant')
  })

  it('clearMessages resets state', async () => {
    apiClient.post.mockResolvedValueOnce({
      data: { answer: 'hi', sources: [] },
    })

    const { messages, clearMessages, sendMessage } = useChat()
    await sendMessage('hello', 'agent-1')
    expect(messages.value).toHaveLength(2)

    clearMessages()
    expect(messages.value).toEqual([])
  })
})
