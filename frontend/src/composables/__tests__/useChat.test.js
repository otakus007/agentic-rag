import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useChat } from '../useChat.js'

// Mock auth module
vi.mock('../../api/auth.js', () => ({
  getToken: vi.fn(() => 'test-token'),
}))

function createMockResponse(events) {
  const encoder = new TextEncoder()
  const chunks = events.map((e) => `data: ${JSON.stringify(e)}\n\n`)
  let index = 0

  const stream = new ReadableStream({
    pull(controller) {
      if (index < chunks.length) {
        controller.enqueue(encoder.encode(chunks[index]))
        index++
      } else {
        controller.close()
      }
    },
  })

  return { ok: true, body: stream }
}

describe('useChat (SSE streaming)', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    global.fetch = vi.fn()
  })

  it('streams tokens into assistant message', async () => {
    global.fetch.mockResolvedValueOnce(
      createMockResponse([
        { type: 'token', content: 'Hello' },
        { type: 'token', content: ' world' },
        { type: 'done' },
      ]),
    )

    const { messages, sendMessage } = useChat()
    await sendMessage('hi', 'agent1')

    expect(messages.value).toHaveLength(2)
    expect(messages.value[0].role).toBe('user')
    expect(messages.value[1].role).toBe('assistant')
    expect(messages.value[1].content).toBe('Hello world')
  })

  it('captures sources from SSE event', async () => {
    global.fetch.mockResolvedValueOnce(
      createMockResponse([
        { type: 'token', content: 'Answer' },
        { type: 'sources', sources: [{ content: 'src', page_number: 1, block_type: 'text' }] },
        { type: 'done' },
      ]),
    )

    const { currentSources, sendMessage } = useChat()
    await sendMessage('q', 'a')

    expect(currentSources.value).toHaveLength(1)
  })

  it('handles fetch errors', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network fail'))

    const { error, messages, sendMessage } = useChat()
    await sendMessage('q', 'a')

    expect(error.value).toBe('Network fail')
    expect(messages.value[1].content).toContain('error')
  })

  it('clears messages', () => {
    const { messages, clearMessages } = useChat()
    messages.value = [{ role: 'user', content: 'hi' }]
    clearMessages()
    expect(messages.value).toHaveLength(0)
  })
})
