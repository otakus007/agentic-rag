import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useKnowledgeBases } from '../useKnowledgeBases.js'

vi.mock('../../api/client.js', () => ({
  default: {
    get: vi.fn(),
    delete: vi.fn(),
  },
}))

import apiClient from '../../api/client.js'

describe('useKnowledgeBases', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetches KB list from API', async () => {
    apiClient.get.mockResolvedValueOnce({
      data: [
        { name: 'kb_agent1', agent_id: 'agent1', document_count: 10 },
        { name: 'kb_agent2', agent_id: 'agent2', document_count: 5 },
      ],
    })

    const { kbs, fetchKBs } = useKnowledgeBases()
    await fetchKBs()

    expect(kbs.value).toHaveLength(2)
    expect(kbs.value[0].agent_id).toBe('agent1')
    expect(apiClient.get).toHaveBeenCalledWith('/admin/kb')
  })

  it('deletes a KB and removes from list', async () => {
    apiClient.delete.mockResolvedValueOnce({ data: { status: 'deleted' } })

    const { kbs, deleteKB } = useKnowledgeBases()
    kbs.value = [
      { name: 'kb_a', agent_id: 'a', document_count: 3 },
      { name: 'kb_b', agent_id: 'b', document_count: 1 },
    ]

    await deleteKB('a')

    expect(kbs.value).toHaveLength(1)
    expect(kbs.value[0].agent_id).toBe('b')
    expect(apiClient.delete).toHaveBeenCalledWith('/admin/kb/a')
  })

  it('captures errors on fetch', async () => {
    apiClient.get.mockRejectedValueOnce(new Error('Network error'))

    const { error, fetchKBs } = useKnowledgeBases()
    await fetchKBs()

    expect(error.value).toBe('Network error')
  })
})
