# Phase 8: User Chat Interface - Implementation Plan

> **For Antigravity:** REQUIRED SUB-SKILL: Load `executing-plans` to implement this plan task-by-task.

**Goal:** Build the end-user chat page with loading skeletons, inline citation markers, sources panel, and conversation sidebar.

**Design:** AI-Native UI style — typing indicators (3-dot pulse), smooth reveals, dark OLED theme. Page overrides in `design-system/agentic-rag/pages/chat.md`.

---

## Verification Plan
`cd frontend && npm run test` must pass after each task.

### Task 1: Chat API Composable & State Management

**Files:**
- Create: `frontend/src/composables/useChat.js`
- Test: `frontend/src/composables/__tests__/useChat.test.js`

<acceptance_criteria>
- `useChat()` returns reactive `messages`, `isLoading`, `error`, `sendMessage()`.
- `sendMessage(text, agentId)` calls `POST /chat` via the API client.
- Response `answer` and `sources` are appended to messages array.
- Loading state is `true` during API call, `false` after.
- Errors are captured in `error` ref without crashing.
</acceptance_criteria>

**Step 1: Write the failing test**
```js
describe('useChat', () => {
  it('sends message and appends response', async () => { ... })
  it('sets isLoading during API call', async () => { ... })
  it('captures errors without crashing', async () => { ... })
})
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(08): add useChat composable with API integration"`

---

### Task 2: Message List with Citation Markers

**Files:**
- Create: `frontend/src/components/MessageList.vue`
- Create: `frontend/src/components/MessageBubble.vue`
- Create: `frontend/src/components/LoadingSkeleton.vue`
- Test: `frontend/src/components/__tests__/MessageBubble.test.js`

<acceptance_criteria>
- `MessageList.vue` renders a scrollable list of messages (user + AI).
- User messages aligned right with surface-light bg. AI messages aligned left.
- `MessageBubble.vue` renders citation markers `[1]`, `[2]` as clickable spans.
- Clicking a citation emits `@cite-click` event with the source index.
- `LoadingSkeleton.vue` shows 3-dot pulse animation during loading.
- Auto-scrolls to bottom on new message.
</acceptance_criteria>

**Step 1: Write the failing test**
```js
describe('MessageBubble', () => {
  it('renders citation markers as clickable elements', () => { ... })
  it('emits cite-click with index on citation click', () => { ... })
})
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(08): add message list with citation markers"`

---

### Task 3: Conversation Sidebar

**Files:**
- Create: `frontend/src/components/ConversationSidebar.vue`
- Create: `frontend/src/composables/useConversations.js`

<acceptance_criteria>
- Sidebar lists conversation sessions with title and date.
- "New chat" button starts a fresh conversation.
- Active conversation is highlighted with CTA border.
- Collapsible on mobile (hamburger toggle).
- Conversations stored in `localStorage` for now (no backend persistence yet).
</acceptance_criteria>

**Step 1: Write minimal implementation**

**Step 2: Commit**
`git commit -m "feat(08): add conversation sidebar"`

---

### Task 4: Sources Panel with Citation Interaction

**Files:**
- Create: `frontend/src/components/SourcesPanel.vue`
- Create: `frontend/src/components/SourceCard.vue`
- Modify: `frontend/src/views/ChatView.vue` (assemble all components)
- Test: `frontend/src/components/__tests__/SourceCard.test.js`

<acceptance_criteria>
- `SourcesPanel.vue` slides in from the right when a citation is clicked.
- Shows list of sources with the clicked one highlighted/scrolled-to.
- `SourceCard.vue` displays: content snippet, page number badge, block type tag.
- Panel has a close button. Clicking outside the panel closes it.
- `ChatView.vue` assembles: sidebar | chat messages + input | sources panel.
- Responsive: sidebar collapses on < 768px, sources panel becomes bottom sheet.
</acceptance_criteria>

**Step 1: Write the failing test**
```js
describe('SourceCard', () => {
  it('renders content, page number, and block type', () => { ... })
  it('highlights when active', () => { ... })
})
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(08): add sources panel with citation interaction"`
