import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useChatbots } from '../useChatbots.js'

vi.mock('../../api/client.js', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}))

import apiClient from '../../api/client.js'

describe('useChatbots', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetches chatbot list from API', async () => {
    apiClient.get.mockResolvedValueOnce({
      data: [
        { id: '1', name: 'Bot A', agent_id: 'a', kb_id: 'kb1', model: 'gpt-4o-mini' },
      ],
    })

    const { chatbots, fetchChatbots } = useChatbots()
    await fetchChatbots()

    expect(chatbots.value).toHaveLength(1)
    expect(chatbots.value[0].name).toBe('Bot A')
    expect(apiClient.get).toHaveBeenCalledWith('/admin/chatbots')
  })

  it('creates a chatbot and prepends to list', async () => {
    apiClient.post.mockResolvedValueOnce({
      data: { id: '2', name: 'New Bot', agent_id: 'b', kb_id: 'kb2', model: 'gpt-4o' },
    })

    const { chatbots, createChatbot } = useChatbots()
    const result = await createChatbot({ name: 'New Bot', agent_id: 'b', kb_id: 'kb2', model: 'gpt-4o' })

    expect(result.name).toBe('New Bot')
    expect(chatbots.value).toHaveLength(1)
  })

  it('deletes a chatbot and removes from list', async () => {
    apiClient.delete.mockResolvedValueOnce({ data: { status: 'deleted' } })

    const { chatbots, deleteChatbot } = useChatbots()
    chatbots.value = [
      { id: '1', name: 'A' },
      { id: '2', name: 'B' },
    ]

    await deleteChatbot('1')
    expect(chatbots.value).toHaveLength(1)
    expect(chatbots.value[0].id).toBe('2')
  })

  it('fetches available models', async () => {
    apiClient.get.mockResolvedValueOnce({
      data: { models: ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo'] },
    })

    const { models, fetchModels } = useChatbots()
    await fetchModels()

    expect(models.value).toEqual(['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo'])
  })
})
