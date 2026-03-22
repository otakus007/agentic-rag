import { ref } from 'vue'
import { getToken } from '../api/auth.js'

export function useChat() {
  const messages = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const currentSources = ref([])

  async function sendMessage(text, agentId) {
    messages.value.push({ role: 'user', content: text })
    isLoading.value = true
    error.value = null
    currentSources.value = []

    // Add placeholder assistant message for streaming
    const assistantMsg = { role: 'assistant', content: '', sources: [] }
    messages.value.push(assistantMsg)

    try {
      const token = getToken()
      const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
      const response = await fetch(`${baseUrl}/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ message: text, agent_id: agentId }),
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          try {
            const event = JSON.parse(line.slice(6))
            if (event.type === 'token') {
              assistantMsg.content += event.content
              // Trigger reactivity
              messages.value = [...messages.value]
            } else if (event.type === 'sources') {
              assistantMsg.sources = event.sources || []
              currentSources.value = event.sources || []
            } else if (event.type === 'error') {
              error.value = event.message
            }
          } catch {
            // skip malformed lines
          }
        }
      }
    } catch (err) {
      error.value = err.message || 'Something went wrong'
      assistantMsg.content = 'Sorry, an error occurred. Please try again.'
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
