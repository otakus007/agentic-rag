# Project Roadmap: Agentic RAG Platform

## v1.0 — Backend Platform (Completed 2026-03-21)
[Full details](milestones/v1.0-ROADMAP.md) | 6 phases | 41 tests | 1,190 LOC

## v1.1 — Frontend UI (Completed 2026-03-22)
[Full details](milestones/v1.1-ROADMAP.md) | 4 phases | 80 tests | 2,570 LOC

---

## v1.2 — Production Polish (Current)

### Phase 11: SSE Streaming Chat
**Goal:** Replace synchronous `/chat` with Server-Sent Events for token-by-token streaming. Update frontend `useChat` to render progressive text. Add dark/light mode toggle.
**Status:** Pending

### Phase 12: Multi-Provider LLM Routing
**Goal:** Create unified LLM adapter interface supporting OpenAI, Gemini, and Anthropic. Dynamic model discovery from provider APIs. Chatbot config selects provider + model.
**Status:** Pending

### Phase 13: User Management & RBAC
**Goal:** Users table, admin/user roles, role-based route guards (backend + frontend). Microsoft OAuth provider. Admin user management UI.
**Status:** Pending

### Phase 14: Ingestion Progress & Document CRUD
**Goal:** SSE-based ingestion progress tracking. Document-level CRUD within knowledge bases (view, search, delete chunks). KB usage analytics.
**Status:** Pending

### Phase 15: API Polish & Migration System
**Goal:** API versioning (v1 prefix), database migration system, provider API key management UI, and final integration testing.
**Status:** Pending
