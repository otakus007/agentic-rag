<template>
  <div
    :class="[
      'border-l border-border bg-surface flex flex-col h-full transition-all duration-300',
      isOpen ? 'w-80' : 'w-0 overflow-hidden'
    ]"
  >
    <!-- Header -->
    <div class="p-4 border-b border-border flex items-center justify-between">
      <h3 class="text-sm font-semibold text-text">Sources</h3>
      <button
        class="p-1 rounded-lg hover:bg-surface-light cursor-pointer text-text-muted"
        @click="$emit('close')"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Sources list -->
    <div class="flex-1 overflow-y-auto p-3 space-y-3">
      <SourceCard
        v-for="(source, i) in sources"
        :key="i"
        :source="source"
        :index="i + 1"
        :active="activeIndex === i + 1"
        :ref="(el) => { if (activeIndex === i + 1 && el?.$el) el.$el.scrollIntoView({ behavior: 'smooth', block: 'center' }) }"
      />

      <div v-if="sources.length === 0" class="text-center text-text-muted text-xs py-8">
        No sources for this message
      </div>
    </div>
  </div>
</template>

<script setup>
import SourceCard from './SourceCard.vue'

defineProps({
  sources: { type: Array, default: () => [] },
  activeIndex: { type: Number, default: 0 },
  isOpen: { type: Boolean, default: false },
})

defineEmits(['close'])
</script>
