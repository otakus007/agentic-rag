<template>
  <AdminLayout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-text">Chatbots</h1>
          <p class="text-sm text-text-muted mt-1">Create and manage your AI chatbot configurations</p>
        </div>
        <button
          class="px-4 py-2 bg-cta text-background font-semibold rounded-xl cursor-pointer hover:bg-cta/80 transition-colors text-sm"
          @click="showCreate = true"
        >
          + New Chatbot
        </button>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="w-8 h-8 mx-auto border-2 border-cta border-t-transparent rounded-full animate-spin"></div>
      </div>

      <!-- Chatbot Grid -->
      <div v-else-if="chatbots.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="bot in chatbots"
          :key="bot.id"
          class="bg-surface border border-border rounded-xl p-4 hover:border-cta/30 transition-colors cursor-pointer"
          @click="openEdit(bot)"
        >
          <div class="flex items-start justify-between mb-3">
            <h3 class="text-sm font-semibold text-text">{{ bot.name }}</h3>
            <span class="text-xs px-2 py-0.5 rounded-full bg-cta/10 text-cta font-medium">{{ bot.model }}</span>
          </div>
          <p class="text-xs text-text-muted line-clamp-2 mb-3">{{ bot.description || 'No description' }}</p>
          <div class="flex items-center gap-3 text-xs text-text-muted">
            <span class="font-mono">KB: {{ bot.kb_id }}</span>
            <span class="ml-auto font-mono">{{ bot.agent_id }}</span>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-16 bg-surface rounded-xl border border-border">
        <svg class="w-12 h-12 mx-auto text-text-muted mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
        <p class="text-text-muted">No chatbots configured yet</p>
        <p class="text-text-muted text-sm mt-1">Create your first chatbot to get started</p>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreate || editBot"
      class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-surface border border-border rounded-2xl p-6 max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h3 class="text-lg font-semibold text-text mb-4">{{ editBot ? 'Edit Chatbot' : 'Create Chatbot' }}</h3>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-text-muted mb-1">Name</label>
            <input v-model="form.name" type="text" required
              class="w-full bg-surface-light border border-border rounded-lg px-3 py-2 text-sm text-text focus:outline-none focus:border-cta" />
          </div>
          <div>
            <label class="block text-xs font-medium text-text-muted mb-1">Description</label>
            <textarea v-model="form.description" rows="2"
              class="w-full bg-surface-light border border-border rounded-lg px-3 py-2 text-sm text-text focus:outline-none focus:border-cta resize-none"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-text-muted mb-1">Agent ID</label>
              <input v-model="form.agent_id" type="text" required
                class="w-full bg-surface-light border border-border rounded-lg px-3 py-2 text-sm text-text font-mono focus:outline-none focus:border-cta" />
            </div>
            <div>
              <label class="block text-xs font-medium text-text-muted mb-1">Knowledge Base ID</label>
              <input v-model="form.kb_id" type="text" required
                class="w-full bg-surface-light border border-border rounded-lg px-3 py-2 text-sm text-text font-mono focus:outline-none focus:border-cta" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-medium text-text-muted mb-1">LLM Model</label>
            <select v-model="form.model"
              class="w-full bg-surface-light border border-border rounded-lg px-3 py-2 text-sm text-text focus:outline-none focus:border-cta cursor-pointer">
              <option v-for="m in models" :key="m" :value="m">{{ m }}</option>
            </select>
          </div>

          <!-- Test Chat Panel (edit mode only) -->
          <div v-if="editBot" class="border-t border-border pt-4">
            <h4 class="text-sm font-semibold text-text mb-2">Test Chat</h4>
            <div class="bg-surface-light rounded-lg p-3 min-h-[100px] max-h-[200px] overflow-y-auto mb-2 text-sm">
              <div v-for="(msg, i) in testMessages" :key="i" :class="msg.role === 'user' ? 'text-cta' : 'text-text'">
                <span class="font-medium">{{ msg.role === 'user' ? 'You' : 'AI' }}:</span> {{ msg.content }}
              </div>
              <div v-if="testLoading" class="text-text-muted">Thinking...</div>
              <div v-if="testMessages.length === 0 && !testLoading" class="text-text-muted">Send a test message</div>
            </div>
            <div class="flex gap-2">
              <input v-model="testInput" type="text" placeholder="Test message..."
                class="flex-1 bg-surface border border-border rounded-lg px-3 py-2 text-sm text-text focus:outline-none focus:border-cta"
                @keydown.enter.prevent="sendTestMessage" />
              <button type="button" @click="sendTestMessage"
                class="px-3 py-2 bg-cta/20 text-cta rounded-lg text-sm font-medium cursor-pointer hover:bg-cta/30"
                :disabled="!testInput.trim() || testLoading">
                Test
              </button>
            </div>
          </div>

          <div class="flex gap-3 justify-end pt-2">
            <button v-if="editBot" type="button" @click="handleDelete"
              class="px-4 py-2 text-sm text-danger hover:text-danger/80 cursor-pointer mr-auto">Delete</button>
            <button type="button" @click="closeModal"
              class="px-4 py-2 text-sm text-text-muted hover:text-text cursor-pointer rounded-lg">Cancel</button>
            <button type="submit"
              class="px-4 py-2 text-sm bg-cta text-background rounded-lg cursor-pointer hover:bg-cta/80 font-medium">
              {{ editBot ? 'Save' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'
import { useChatbots } from '../../composables/useChatbots.js'
import { useChat } from '../../composables/useChat.js'

const { chatbots, models, isLoading, fetchChatbots, fetchModels, createChatbot, updateChatbot, deleteChatbot } = useChatbots()

const showCreate = ref(false)
const editBot = ref(null)
const form = reactive({ name: '', description: '', agent_id: '', kb_id: '', model: 'gpt-4o-mini' })

// Test chat
const { messages: testMessages, isLoading: testLoading, sendMessage: sendTestMsg, clearMessages } = useChat()
const testInput = ref('')

function openEdit(bot) {
  editBot.value = bot
  Object.assign(form, { name: bot.name, description: bot.description, agent_id: bot.agent_id, kb_id: bot.kb_id, model: bot.model })
  clearMessages()
}

function closeModal() {
  showCreate.value = false
  editBot.value = null
  Object.assign(form, { name: '', description: '', agent_id: '', kb_id: '', model: 'gpt-4o-mini' })
  clearMessages()
}

async function handleSubmit() {
  try {
    if (editBot.value) {
      await updateChatbot(editBot.value.id, { ...form })
    } else {
      await createChatbot({ ...form })
    }
    closeModal()
  } catch (err) {
    // Error handled by composable
  }
}

async function handleDelete() {
  if (editBot.value) {
    await deleteChatbot(editBot.value.id)
    closeModal()
  }
}

function sendTestMessage() {
  if (!testInput.value.trim() || testLoading.value) return
  sendTestMsg(testInput.value.trim(), form.agent_id)
  testInput.value = ''
}

onMounted(() => {
  fetchChatbots()
  fetchModels()
})
</script>
