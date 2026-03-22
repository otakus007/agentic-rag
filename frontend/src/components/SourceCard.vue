<template>
  <div :class="[
    'rounded-xl p-3 border transition-colors',
    active
      ? 'bg-cta/10 border-cta/40'
      : 'bg-surface-light border-border hover:border-border/80'
  ]">
    <div class="flex items-center gap-2 mb-2">
      <span class="inline-flex items-center justify-center w-6 h-6 text-xs font-bold rounded-lg bg-cta/20 text-cta">
        {{ index }}
      </span>
      <span class="text-xs px-2 py-0.5 rounded-full bg-surface border border-border text-text-muted">
        {{ source.block_type || 'text' }}
      </span>
      <span class="text-xs text-text-muted ml-auto">
        p. {{ source.page_number }}
      </span>
    </div>
    <p class="text-sm text-text leading-relaxed line-clamp-4">
      {{ source.content }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  source: { type: Object, required: true },
  index: { type: Number, required: true },
  active: { type: Boolean, default: false },
})
</script>
