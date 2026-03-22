# Phase 7: Frontend Scaffold & Design System - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary
Initialize Vue 3 + Vite + Tailwind project in `frontend/`. Set up UUPM design system, API client module with JWT token management, and routing structure.
</domain>

<decisions>
## Implementation Decisions

### Project Structure
- Separate `frontend/` directory with its own `package.json`.
- Backend stays in `src/` with Poetry — no monorepo tooling.
- Two independent projects sharing the same git repo.

### Routing & Page Layout
- Vue Router with 3 route groups:
  - `/login` — public OAuth login page
  - `/chat` — user chat interface (sidebar navigation)
  - `/admin/*` — admin pages (top navigation)
- Shared app shell with `<RouterView>`.
- Navigation guards for auth-required routes.

### API Client & Auth Flow
- Redirect-based OAuth — frontend redirects to Google/Microsoft.
- On callback, receive JWT token and store in `localStorage`.
- Axios instance with interceptor to attach Bearer token to all API calls.
- Backend needs new `/auth/callback` endpoint (small addition in this phase).
- Auto-redirect to `/login` on 401 responses.
</decisions>

<canonical_refs>
## Canonical References
- `src/main.py` — Backend FastAPI endpoints (`/chat`, `/ingest`, `/health`).
- `src/auth/providers.py` — JWT verification (Google/Microsoft).
- `.agent/skills/ui-ux-pro-max/SKILL.md` — UUPM design system workflow.
</canonical_refs>

<code_context>
## Existing Code Insights
### Backend API Surface
- `GET /health` — public, no auth
- `POST /chat` — requires Bearer, body: `{message, agent_id}`, returns `{answer, sources[]}`
- `POST /ingest` — requires Bearer, multipart: `file` + query: `agent_id`
### UUPM Integration
- Generate design system: `python3 .agent/skills/ui-ux-pro-max/scripts/search.py "RAG chatbot SaaS" --design-system --persist --stack vue -p "Agentic RAG"`
- Vue stack guidelines: `--stack vue`
</code_context>

<deferred>
## Deferred Ideas
- WebSocket/SSE streaming for real-time chat (Phase 8 consideration)
- PWA service worker for offline shell
- i18n internationalization
</deferred>

---
*Phase: 07-frontend-scaffold-design-system*
*Context gathered: 2026-03-22*
