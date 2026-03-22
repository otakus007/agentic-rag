import { ref } from 'vue'
import apiClient from '../api/client.js'

export function useChat() {
  const messages = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const currentSources = ref([])

  async function sendMessage(text, agentId) {
    // Add user message
    messages.value.push({ role: 'user', content: text })
    isLoading.value = true
    error.value = null
    currentSources.value = []

    try {
      const response = await apiClient.post('/chat', {
        message: text,
        agent_id: agentId,
      })

      const { answer, sources } = response.data
      currentSources.value = sources || []

      messages.value.push({
        role: 'assistant',
        content: answer,
        sources: sources || [],
      })
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Something went wrong'
      messages.value.push({
        role: 'assistant',
        content: 'Sorry, an error occurred. Please try again.',
        sources: [],
      })
    } finally {
      isLoading.value = false
    }
  }

  function clearMessages() {
    messages.value = []
    currentSources.value = []
    error.value = null
  }

  return {
    messages,
    isLoading,
    error,
    currentSources,
    sendMessage,
    clearMessages,
  }
}
