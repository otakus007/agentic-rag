<template>
  <AdminLayout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-text">Knowledge Bases</h1>
          <p class="text-sm text-text-muted mt-1">Manage your Qdrant document collections</p>
        </div>
      </div>

      <!-- Upload zone -->
      <FileUploadZone @upload-complete="fetchKBs" />

      <!-- Loading state -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="w-8 h-8 mx-auto border-2 border-cta border-t-transparent rounded-full animate-spin"></div>
        <p class="text-text-muted text-sm mt-3">Loading knowledge bases...</p>
      </div>

      <!-- KB Table -->
      <div v-else-if="kbs.length > 0" class="bg-surface rounded-xl border border-border overflow-hidden">
        <table class="w-full">
          <thead>
            <tr class="border-b border-border">
              <th class="text-left text-xs font-semibold text-text-muted px-4 py-3 uppercase tracking-wider">Name</th>
              <th class="text-left text-xs font-semibold text-text-muted px-4 py-3 uppercase tracking-wider">Agent ID</th>
              <th class="text-left text-xs font-semibold text-text-muted px-4 py-3 uppercase tracking-wider">Documents</th>
              <th class="text-right text-xs font-semibold text-text-muted px-4 py-3 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="kb in kbs"
              :key="kb.agent_id"
              class="border-b border-border/50 hover:bg-surface-light transition-colors"
            >
              <td class="px-4 py-3 text-sm text-text font-medium">{{ kb.name }}</td>
              <td class="px-4 py-3 text-sm text-text-muted font-mono">{{ kb.agent_id }}</td>
              <td class="px-4 py-3">
                <span :class="[
                  'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
                  kb.document_count > 0
                    ? 'bg-cta/10 text-cta'
                    : 'bg-border/30 text-text-muted'
                ]">
                  {{ kb.document_count }} docs
                </span>
              </td>
              <td class="px-4 py-3 text-right">
                <button
                  class="text-xs text-danger hover:text-danger/80 cursor-pointer font-medium"
                  @click="confirmDelete(kb)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-16 bg-surface rounded-xl border border-border">
        <svg class="w-12 h-12 mx-auto text-text-muted mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
        </svg>
        <p class="text-text-muted">No knowledge bases yet</p>
        <p class="text-text-muted text-sm mt-1">Upload PDF files above to create your first KB</p>
      </div>

      <!-- Error -->
      <div v-if="error" class="bg-danger/10 border border-danger/30 rounded-xl px-4 py-3 text-sm text-danger">
        {{ error }}
      </div>
    </div>

    <!-- Delete confirmation dialog -->
    <div
      v-if="deleteTarget"
      class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      @click.self="deleteTarget = null"
    >
      <div class="bg-surface border border-border rounded-2xl p-6 max-w-sm w-full mx-4">
        <h3 class="text-lg font-semibold text-text mb-2">Delete Knowledge Base</h3>
        <p class="text-sm text-text-muted mb-4">
          Are you sure you want to delete <strong>{{ deleteTarget.name }}</strong>?
          This will remove all {{ deleteTarget.document_count }} documents permanently.
        </p>
        <div class="flex gap-3 justify-end">
          <button
            class="px-4 py-2 text-sm text-text-muted hover:text-text cursor-pointer rounded-lg"
            @click="deleteTarget = null"
          >
            Cancel
          </button>
          <button
            class="px-4 py-2 text-sm bg-danger text-white rounded-lg cursor-pointer hover:bg-danger/80"
            @click="executeDelete"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'
import FileUploadZone from '../../components/FileUploadZone.vue'
import { useKnowledgeBases } from '../../composables/useKnowledgeBases.js'

const { kbs, isLoading, error, fetchKBs, deleteKB } = useKnowledgeBases()

const deleteTarget = ref(null)

function confirmDelete(kb) {
  deleteTarget.value = kb
}

async function executeDelete() {
  if (deleteTarget.value) {
    await deleteKB(deleteTarget.value.agent_id)
    deleteTarget.value = null
  }
}

onMounted(fetchKBs)
</script>
