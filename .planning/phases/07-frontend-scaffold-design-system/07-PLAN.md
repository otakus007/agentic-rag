# Phase 7: Frontend Scaffold & Design System - Implementation Plan

> **For Antigravity:** REQUIRED SUB-SKILL: Load `executing-plans` to implement this plan task-by-task.

**Goal:** Initialize Vue 3 + Vite + Tailwind in `frontend/`, apply UUPM design system, create API client with JWT management, and set up Vue Router with auth guards.

**Design System:** Dark Mode OLED — Primary `#0F172A`, BG `#020617`, CTA `#22C55E`, Text `#F8FAFC`, Font: Plus Jakarta Sans. Persisted in `design-system/agentic-rag/MASTER.md`.

---

## Verification Plan
Frontend tests via Vitest. `cd frontend && npm run test` must pass after each task.

### Task 1: Vue 3 + Vite + Tailwind Initialization

**Files:**
- Create: `frontend/` (via `npx create-vite`)
- Create: `frontend/tailwind.config.js`, `frontend/postcss.config.js`
- Modify: `frontend/src/style.css` (Tailwind directives)

<acceptance_criteria>
- `npm create vite@latest frontend/ -- --template vue` scaffolds the project.
- Tailwind CSS installed and configured with UUPM design tokens (colors, fonts).
- `npm run dev` starts dev server without errors.
- `npm run build` produces production bundle.
- Plus Jakarta Sans loaded from Google Fonts.
</acceptance_criteria>

**Step 1: Scaffold and configure**
```bash
cd frontend && npm install -D tailwindcss @tailwindcss/vite
```

**Step 2: Apply UUPM design tokens to `tailwind.config.js`**
```js
// Extend theme with design system colors
colors: {
  primary: '#0F172A',
  secondary: '#1E293B',
  cta: '#22C55E',
  background: '#020617',
  surface: '#0F172A',
}
```

**Step 3: Commit**
`git commit -m "feat(07): initialize Vue 3 + Vite + Tailwind frontend"`

---

### Task 2: API Client with JWT Token Management

**Files:**
- Create: `frontend/src/api/client.js`
- Create: `frontend/src/api/auth.js`
- Test: `frontend/src/api/__tests__/client.test.js`

<acceptance_criteria>
- Axios instance with `baseURL` from env var (`VITE_API_URL`).
- Request interceptor attaches `Authorization: Bearer <token>` from `localStorage`.
- Response interceptor redirects to `/login` on 401.
- `auth.js` exports `login()`, `logout()`, `getToken()`, `isAuthenticated()`.
- Token stored/retrieved from `localStorage`.
</acceptance_criteria>

**Step 1: Write the failing test**
```js
// frontend/src/api/__tests__/client.test.js
import { describe, it, expect, vi } from 'vitest'

describe('API Client', () => {
  it('attaches Bearer token to requests', () => { ... })
  it('redirects to /login on 401', () => { ... })
})

describe('Auth', () => {
  it('getToken returns token from localStorage', () => { ... })
  it('isAuthenticated returns false when no token', () => { ... })
})
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(07): add API client with JWT token management"`

---

### Task 3: Vue Router with Navigation Guards

**Files:**
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/views/LoginView.vue` (placeholder)
- Create: `frontend/src/views/ChatView.vue` (placeholder)
- Create: `frontend/src/views/admin/DashboardView.vue` (placeholder)
- Modify: `frontend/src/App.vue`
- Test: `frontend/src/router/__tests__/router.test.js`

<acceptance_criteria>
- Routes: `/login` (public), `/chat` (requires auth), `/admin` (requires auth).
- Navigation guard redirects to `/login` if not authenticated.
- `/login` redirects to `/chat` if already authenticated.
- `App.vue` renders `<RouterView>` inside a layout shell.
</acceptance_criteria>

**Step 1: Write the failing test**
```js
describe('Router', () => {
  it('redirects unauthenticated users to /login', () => { ... })
  it('allows authenticated users to access /chat', () => { ... })
})
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(07): add Vue Router with auth navigation guards"`

---

### Task 4: App Shell & Layout Components

**Files:**
- Create: `frontend/src/layouts/AppLayout.vue`
- Create: `frontend/src/components/Sidebar.vue`
- Create: `frontend/src/components/TopNav.vue`
- Modify: `frontend/src/App.vue`

<acceptance_criteria>
- `AppLayout.vue` wraps content with sidebar (chat routes) or top nav (admin routes).
- Dark mode applied by default using UUPM design tokens.
- Responsive: sidebar collapses on mobile.
- UUPM pre-delivery checklist items satisfied (no emojis as icons, cursor-pointer, smooth transitions).
</acceptance_criteria>

**Step 1: Build layout components with UUPM tokens**

**Step 2: Verify responsive behavior at 375px, 768px, 1024px, 1440px**

**Step 3: Commit**
`git commit -m "feat(07): add app shell with sidebar and top nav layouts"`
