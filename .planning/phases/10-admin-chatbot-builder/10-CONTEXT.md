# Phase 10: Admin Chatbot Builder - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary
Create/list/edit chatbots with KB assignment and LLM model selection, plus admin test-chat panel.
</domain>

<decisions>
## Implementation Decisions

### Chatbot Persistence
- Use existing Postgres pool from `lifespan`.
- Single `chatbots` table: `id` (UUID), `name`, `description`, `agent_id` (unique), `kb_id`, `model`, `created_at`.
- Simple SQL via psycopg — no ORM needed.
- Backend CRUD: `POST /admin/chatbots`, `GET /admin/chatbots`, `GET /admin/chatbots/{id}`, `PUT /admin/chatbots/{id}`, `DELETE /admin/chatbots/{id}`.

### LLM Model Selection
- Hardcoded list in v1.1: `["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]`.
- Model stored in chatbot config row.
- Backend passes `model` to agent graph at invoke time.
- Dynamic model discovery deferred to v1.2.

### Test Chat Panel
- Lightweight test panel embedded in chatbot edit/detail page.
- Simple textarea + "Send" button + response display area.
- Reuse `useChat` composable, skip conversation sidebar and sources panel.
- Focus on quick verification.
</decisions>

<canonical_refs>
## Canonical References
- `src/main.py` — Backend with `/chat`, `/ingest`, `/admin/kb` endpoints.
- `frontend/src/composables/useChat.js` — Reusable chat composable.
- `frontend/src/components/AdminTopNav.vue` — Chatbots tab already exists.
- `frontend/src/views/admin/DashboardView.vue` — Placeholder for `/admin/chatbots`.
- `frontend/src/router/index.js` — `/admin/chatbots` route exists.
</canonical_refs>

<deferred>
## Deferred Ideas
- Dynamic LLM model discovery from provider APIs (v1.2).
- Chatbot versioning and rollback.
- System prompt customization per chatbot.
- Chatbot analytics and usage tracking.
</deferred>
