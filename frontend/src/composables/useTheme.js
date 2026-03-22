import { ref, watch } from 'vue'

const STORAGE_KEY = 'agentic-rag-theme'

export function useTheme() {
  const theme = ref(localStorage.getItem(STORAGE_KEY) || 'dark')

  function apply(t) {
    document.documentElement.setAttribute('data-theme', t)
    localStorage.setItem(STORAGE_KEY, t)
  }

  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  watch(theme, apply, { immediate: true })

  return { theme, toggle }
}
