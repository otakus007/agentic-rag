<template>
  <div class="min-h-screen bg-background text-text flex flex-col">
    <AdminTopNav />
    <main class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">
      <slot />
    </main>
  </div>
</template>

<script setup>
import AdminTopNav from '../components/AdminTopNav.vue'
</script>
