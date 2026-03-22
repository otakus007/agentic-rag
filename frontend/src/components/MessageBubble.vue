<template>
  <div :class="[
    'max-w-[80%] rounded-2xl px-4 py-3',
    isUser ? 'ml-auto bg-cta/20 text-text' : 'mr-auto bg-surface-light text-text'
  ]">
    <p class="text-xs font-medium mb-1" :class="isUser ? 'text-cta' : 'text-text-muted'">
      {{ isUser ? 'You' : 'Assistant' }}
    </p>
    <div class="text-sm leading-relaxed whitespace-pre-wrap" v-html="renderedContent"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  message: { type: Object, required: true },
})

const emit = defineEmits(['cite-click'])

const isUser = computed(() => props.message.role === 'user')

const renderedContent = computed(() => {
  const text = props.message.content || ''
  // Replace [1], [2], etc. with clickable spans
  return text.replace(
    /\[(\d+)\]/g,
    (match, num) =>
      `<span class="inline-flex items-center justify-center w-5 h-5 text-xs font-bold rounded bg-cta/30 text-cta cursor-pointer hover:bg-cta/50 transition-colors" data-cite="${num}" onclick="this.dispatchEvent(new CustomEvent('cite-click', { bubbles: true, detail: ${num} }))">${num}</span>`
  )
})
</script>
