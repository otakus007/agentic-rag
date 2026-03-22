<template>
  <div
    class="border-2 border-dashed rounded-xl p-8 text-center transition-colors"
    :class="isDragging
      ? 'border-cta bg-cta/5'
      : 'border-border hover:border-cta/50'"
    @dragover.prevent="isDragging = true"
    @dragleave="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <svg class="w-10 h-10 mx-auto text-text-muted mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
    </svg>
    <p class="text-sm text-text mb-1">
      <span class="text-cta font-medium cursor-pointer" @click="openPicker">Browse files</span>
      or drag and drop PDF files here
    </p>
    <p class="text-xs text-text-muted">PDF files only</p>

    <input
      ref="fileInput"
      type="file"
      accept=".pdf"
      multiple
      class="hidden"
      @change="handleFileSelect"
    />

    <!-- Agent ID input -->
    <div class="mt-4 max-w-xs mx-auto">
      <input
        v-model="agentId"
        type="text"
        placeholder="Agent ID (e.g., my-kb)"
        class="w-full bg-surface-light border border-border rounded-lg px-3 py-2 text-sm text-text placeholder-text-muted focus:outline-none focus:border-cta text-center"
      />
    </div>

    <!-- Upload list -->
    <div v-if="uploads.length > 0" class="mt-4 space-y-2 max-w-md mx-auto text-left">
      <div
        v-for="(file, i) in uploads"
        :key="i"
        class="flex items-center gap-3 bg-surface-light rounded-lg px-3 py-2"
      >
        <svg class="w-4 h-4 text-text-muted flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span class="text-sm text-text truncate flex-1">{{ file.name }}</span>
        <span :class="[
          'text-xs font-medium px-2 py-0.5 rounded-full',
          file.status === 'done' ? 'bg-cta/10 text-cta' :
          file.status === 'error' ? 'bg-danger/10 text-danger' :
          'bg-warning/10 text-warning'
        ]">
          {{ file.status }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import apiClient from '../api/client.js'

const emit = defineEmits(['upload-complete'])

const isDragging = ref(false)
const agentId = ref('')
const uploads = ref([])
const fileInput = ref(null)

function openPicker() {
  fileInput.value?.click()
}

function handleFileSelect(event) {
  const files = Array.from(event.target.files || [])
  processFiles(files)
}

function handleDrop(event) {
  isDragging.value = false
  const files = Array.from(event.dataTransfer.files || [])
  processFiles(files)
}

async function processFiles(files) {
  const pdfFiles = files.filter((f) => f.name.toLowerCase().endsWith('.pdf'))
  if (!pdfFiles.length) return
  if (!agentId.value.trim()) {
    agentId.value = 'default'
  }

  for (const file of pdfFiles) {
    const entry = { name: file.name, status: 'uploading' }
    uploads.value.push(entry)

    try {
      const formData = new FormData()
      formData.append('file', file)
      await apiClient.post(`/ingest?agent_id=${agentId.value}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      entry.status = 'done'
      emit('upload-complete')
    } catch (err) {
      entry.status = 'error'
    }
  }
}
</script>
