<template>
  <div class="flex h-screen bg-background">
    <!-- Sidebar toggle (mobile) -->
    <button
      class="fixed top-4 left-4 z-50 p-2 rounded-xl bg-surface border border-border cursor-pointer text-text-muted hover:text-text md:hidden"
      @click="sidebarOpen = !sidebarOpen"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>

    <!-- Conversation Sidebar -->
    <ConversationSidebar
      :conversations="conversations"
      :active-id="activeConversationId"
      :is-open="sidebarOpen"
      @select="selectConversation"
      @new-chat="newChat"
    />

    <!-- Main Chat Area -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Top bar -->
      <div class="h-14 border-b border-border flex items-center px-4 bg-surface">
        <h1 class="text-sm font-semibold text-text truncate">Agentic RAG Chat</h1>
        <button
          v-if="!sidebarOpen"
          class="ml-2 p-1 rounded-lg hover:bg-surface-light cursor-pointer text-text-muted hidden md:block"
          @click="sidebarOpen = true"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      <!-- Messages -->
      <MessageList
        :messages="messages"
        :is-loading="isLoading"
        @cite-click="handleCiteClick"
      />

      <!-- Input -->
      <div class="p-4 border-t border-border bg-surface">
        <form @submit.prevent="handleSend" class="flex gap-3">
          <input
            id="chat-input"
            v-model="inputText"
            type="text"
            placeholder="Ask a question..."
            class="flex-1 bg-surface-light border border-border rounded-xl px-4 py-3 text-sm text-text placeholder-text-muted focus:outline-none focus:border-cta"
            :disabled="isLoading"
          />
          <button
            id="btn-send"
            type="submit"
            class="px-5 py-3 bg-cta text-background font-semibold rounded-xl cursor-pointer hover:bg-cta/80 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            :disabled="!inputText.trim() || isLoading"
          >
            Send
          </button>
        </form>
      </div>
    </div>

    <!-- Sources Panel -->
    <SourcesPanel
      :sources="activeSources"
      :active-index="activeCiteIndex"
      :is-open="sourcesPanelOpen"
      @close="sourcesPanelOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ConversationSidebar from '../components/ConversationSidebar.vue'
import MessageList from '../components/MessageList.vue'
import SourcesPanel from '../components/SourcesPanel.vue'
import { useChat } from '../composables/useChat.js'

const { messages, isLoading, error, currentSources, sendMessage, clearMessages } = useChat()

const inputText = ref('')
const sidebarOpen = ref(true)
const sourcesPanelOpen = ref(false)
const activeCiteIndex = ref(0)
const activeSources = ref([])

// Conversation management (localStorage for now)
const conversations = ref(JSON.parse(localStorage.getItem('conversations') || '[]'))
const activeConversationId = ref(conversations.value[0]?.id || '')

const agentId = ref('default')

function handleSend() {
  if (!inputText.value.trim() || isLoading.value) return
  const text = inputText.value.trim()
  inputText.value = ''
  sendMessage(text, agentId.value)
}

function handleCiteClick(index, sources) {
  activeSources.value = sources || currentSources.value
  activeCiteIndex.value = index
  sourcesPanelOpen.value = true
}

function newChat() {
  clearMessages()
  const id = Date.now().toString()
  const conv = { id, title: 'New chat', date: new Date().toLocaleDateString() }
  conversations.value.unshift(conv)
  activeConversationId.value = id
  saveConversations()
}

function selectConversation(id) {
  activeConversationId.value = id
  clearMessages()
}

function saveConversations() {
  localStorage.setItem('conversations', JSON.stringify(conversations.value))
}
</script>
