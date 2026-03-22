<template>
  <aside :class="[
    'bg-surface border-r border-border flex flex-col h-full transition-all duration-300',
    isOpen ? 'w-64' : 'w-0 overflow-hidden'
  ]">
    <!-- Header -->
    <div class="p-4 border-b border-border flex items-center justify-between">
      <h2 class="text-sm font-semibold text-text">Conversations</h2>
      <button
        class="p-1.5 rounded-lg hover:bg-surface-light cursor-pointer text-text-muted"
        @click="$emit('new-chat')"
        title="New chat"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>
    </div>

    <!-- Conversation list -->
    <div class="flex-1 overflow-y-auto p-2 space-y-1">
      <button
        v-for="conv in conversations"
        :key="conv.id"
        :class="[
          'w-full text-left px-3 py-2.5 rounded-xl text-sm cursor-pointer transition-colors',
          conv.id === activeId
            ? 'bg-cta/10 border border-cta/30 text-text'
            : 'text-text-muted hover:bg-surface-light hover:text-text'
        ]"
        @click="$emit('select', conv.id)"
      >
        <p class="truncate font-medium">{{ conv.title }}</p>
        <p class="text-xs mt-0.5 opacity-60">{{ conv.date }}</p>
      </button>

      <div v-if="conversations.length === 0" class="text-center text-text-muted text-xs py-8">
        No conversations yet
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  conversations: { type: Array, default: () => [] },
  activeId: { type: String, default: '' },
  isOpen: { type: Boolean, default: true },
})

defineEmits(['select', 'new-chat'])
</script>
