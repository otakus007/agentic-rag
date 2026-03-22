# Project Roadmap: Agentic RAG Platform

## v1.0 — Backend Platform (Completed 2026-03-21)
[Full details](milestones/v1.0-ROADMAP.md) | 6 phases | 41 tests | 1,190 LOC

## v1.1 — Frontend UI (Completed 2026-03-22)
[Full details](milestones/v1.1-ROADMAP.md) | 4 phases | 80 tests | 2,570 LOC

## v1.2 — Production Polish (Completed 2026-03-22)
[Full details](milestones/v1.2-ROADMAP.md) | 5 phases | 89 tests | 2,980 LOC

---

## v1.3 — Admin Polish (Current)

### Phase 16: Provider API Key Management
**Goal:** Admin settings page for managing LLM provider API keys. Secure encrypted storage in PostgreSQL. Per-provider key status indicators. Frontend CRUD form.
**Status:** Pending

### Phase 17: KB Usage Analytics
**Goal:** Track query count and most-retrieved chunks per KB. Query log table in PostgreSQL. Analytics dashboard widget on admin KB detail page.
**Status:** Pending

### Phase 18: Custom System Prompts
**Goal:** Add system prompt field to chatbot config. Store in chatbots table. Pass to LLM adapter during invocation. Default template for new chatbots.
**Status:** Pending
