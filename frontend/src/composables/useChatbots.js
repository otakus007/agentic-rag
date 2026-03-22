import { ref } from 'vue'
import apiClient from '../api/client.js'

export function useChatbots() {
  const chatbots = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const models = ref([])

  async function fetchChatbots() {
    isLoading.value = true
    error.value = null
    try {
      const response = await apiClient.get('/admin/chatbots')
      chatbots.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      isLoading.value = false
    }
  }

  async function fetchModels() {
    try {
      const response = await apiClient.get('/admin/models')
      models.value = response.data.models
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    }
  }

  async function createChatbot(data) {
    const response = await apiClient.post('/admin/chatbots', data)
    chatbots.value.unshift(response.data)
    return response.data
  }

  async function updateChatbot(id, data) {
    const response = await apiClient.put(`/admin/chatbots/${id}`, data)
    const idx = chatbots.value.findIndex((c) => c.id === id)
    if (idx >= 0) chatbots.value[idx] = response.data
    return response.data
  }

  async function deleteChatbot(id) {
    await apiClient.delete(`/admin/chatbots/${id}`)
    chatbots.value = chatbots.value.filter((c) => c.id !== id)
  }

  return { chatbots, models, isLoading, error, fetchChatbots, fetchModels, createChatbot, updateChatbot, deleteChatbot }
}
