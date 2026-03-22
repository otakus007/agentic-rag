# Phase 8: User Chat Interface - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary
Build the end-user chat page with streaming responses, inline citation markers, sources panel, dark/light mode, and OAuth login flow.
</domain>

<decisions>
## Implementation Decisions

### Response Delivery
- Start with full-response + loading skeleton animation.
- No SSE streaming in v1.1 — backend returns complete response synchronously.
- Streaming deferred to v1.2 (requires backend refactoring to yield tokens).

### Chat Layout & UX
- Three-column layout:
  - **Left:** Conversation sidebar (collapsible) — list of past sessions.
  - **Center:** Chat messages area with input at bottom.
  - **Right:** Sources panel (slides open on citation click).
- Mobile: sidebar hidden by default, sources as a bottom sheet overlay.
- Dark mode is default (UUPM OLED theme). Light mode toggle deferred.

### Citation Interaction
- Click `[1]` marker in AI answer → right panel slides open with source highlighted.
- Source card shows: content snippet, page number, block type.
- Hover over `[1]` → tooltip with brief content preview.
</decisions>

<canonical_refs>
## Canonical References
- `frontend/src/api/client.js` — Axios API client with JWT interceptor.
- `frontend/src/api/auth.js` — Token CRUD for localStorage.
- `frontend/src/router/index.js` — Vue Router with `/chat` route.
- `frontend/src/style.css` — UUPM dark theme tokens.
- `src/main.py` — Backend `/chat` endpoint returning `{answer, sources[]}`.
- `design-system/agentic-rag/MASTER.md` — UUPM design system.
</canonical_refs>

<code_context>
## Existing Code Insights
### Backend API Contract
- `POST /chat` — body: `{message, agent_id}` → response: `{answer: str, sources: [{content, page_number, block_type}]}`
- Requires Bearer token (JWT from OAuth).
### Frontend Assets
- `ChatView.vue` — placeholder, ready to be replaced.
- API client with interceptors already configured.
- UUPM colors: BG `#020617`, Surface `#0F172A`, CTA `#22C55E`, Text `#F8FAFC`.
</code_context>

<deferred>
## Deferred Ideas
- SSE/WebSocket streaming for token-by-token responses (v1.2).
- Light mode theme toggle.
- Message editing and regeneration.
- File attachments in chat.
</deferred>

---
*Phase: 08-user-chat-interface*
*Context gathered: 2026-03-22*
