<template>
  <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="listRef">
    <div v-if="messages.length === 0" class="flex items-center justify-center h-full">
      <div class="text-center">
        <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-surface-light flex items-center justify-center">
          <svg class="w-8 h-8 text-cta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </div>
        <p class="text-text-muted text-lg">Start a conversation</p>
        <p class="text-text-muted text-sm mt-1">Ask anything about your knowledge base</p>
      </div>
    </div>

    <MessageBubble
      v-for="(msg, i) in messages"
      :key="i"
      :message="msg"
      @cite-click="(idx) => $emit('cite-click', idx, msg.sources)"
    />

    <LoadingSkeleton v-if="isLoading" />
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import MessageBubble from './MessageBubble.vue'
import LoadingSkeleton from './LoadingSkeleton.vue'

const props = defineProps({
  messages: { type: Array, required: true },
  isLoading: { type: Boolean, default: false },
})

defineEmits(['cite-click'])

const listRef = ref(null)

watch(
  () => props.messages.length,
  async () => {
    await nextTick()
    if (listRef.value) {
      listRef.value.scrollTop = listRef.value.scrollHeight
    }
  }
)
</script>
