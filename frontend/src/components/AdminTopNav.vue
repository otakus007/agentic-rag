<template>
  <nav class="bg-surface border-b border-border">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center h-14 gap-6">
        <span class="text-sm font-bold text-cta">Admin</span>

        <router-link
          to="/admin/kb"
          class="text-sm font-medium px-3 py-1.5 rounded-lg transition-colors"
          :class="$route.path.startsWith('/admin/kb')
            ? 'bg-cta/10 text-cta'
            : 'text-text-muted hover:text-text hover:bg-surface-light'"
        >
          Knowledge Bases
        </router-link>

        <router-link
          to="/admin/chatbots"
          class="text-sm font-medium px-3 py-1.5 rounded-lg transition-colors"
          :class="$route.path.startsWith('/admin/chatbots')
            ? 'bg-cta/10 text-cta'
            : 'text-text-muted hover:text-text hover:bg-surface-light'"
        >
          Chatbots
        </router-link>

        <router-link
          to="/chat"
          class="ml-auto text-sm text-text-muted hover:text-text transition-colors"
        >
          ← Back to Chat
        </router-link>
      </div>
    </div>
  </nav>
</template>
