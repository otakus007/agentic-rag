import { ref } from 'vue'
import apiClient from '../api/client.js'

export function useKnowledgeBases() {
  const kbs = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  async function fetchKBs() {
    isLoading.value = true
    error.value = null
    try {
      const response = await apiClient.get('/admin/kb')
      kbs.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      isLoading.value = false
    }
  }

  async function deleteKB(agentId) {
    try {
      await apiClient.delete(`/admin/kb/${agentId}`)
      kbs.value = kbs.value.filter((kb) => kb.agent_id !== agentId)
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    }
  }

  return { kbs, isLoading, error, fetchKBs, deleteKB }
}
