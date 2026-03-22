# Phase 9: Admin — KB Management - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary
Create admin dashboard for uploading PDFs, viewing Qdrant collections, monitoring ingestion status, and managing knowledge bases.
</domain>

<decisions>
## Implementation Decisions

### Backend Admin API
- Add 3 lean endpoints to `src/main.py`:
  - `GET /admin/kb` — list all Qdrant collections with document count.
  - `GET /admin/kb/{agent_id}` — collection details (points count, vector config).
  - `DELETE /admin/kb/{agent_id}` — drop the entire collection.
- All admin endpoints require auth (`Depends(get_current_user)`).
- No document-level CRUD — only collection-level management for v1.1.

### Upload UX
- Drag-and-drop zone accepting multiple PDF files.
- Each file triggers an independent `POST /ingest` call.
- Frontend tracks upload + ingestion status per file.
- No backend job queue — leverage existing FastAPI BackgroundTasks.

### Admin Layout
- Top nav with "Knowledge Bases" and "Chatbots" tabs.
- Separate `AdminLayout.vue` from the chat sidebar layout.
- Admin pages at `/admin/kb` and `/admin/chatbots`.
- Clean, data-focused design — tables, cards, status badges.
</decisions>

<canonical_refs>
## Canonical References
- `src/main.py` — Existing `/ingest` endpoint.
- `src/ingestion/embedder.py` — `get_qdrant_client()`, `embed_and_upsert()`, collection naming `kb_{agent_id}`.
- `frontend/src/api/client.js` — Axios API client with JWT.
- `frontend/src/router/index.js` — `/admin` route.
- `frontend/src/views/admin/DashboardView.vue` — placeholder, ready to replace.
</canonical_refs>

<code_context>
## Existing Code Insights
### Qdrant Collection Pattern
- Collections named `kb_{agent_id}`.
- `qdrant.get_collections()` returns all collections.
- `qdrant.count()` returns point count per collection.
- `qdrant.delete_collection()` drops a collection.
### Upload Flow
- `POST /ingest` accepts multipart file + `agent_id` query param.
- Returns `{status: "ingestion_started", filename: str}` immediately (202).
- Parsing + embedding runs in BackgroundTasks.
</code_context>

<deferred>
## Deferred Ideas
- Ingestion progress polling via WebSocket/SSE (v1.2).
- Document-level CRUD (view/delete individual chunks).
- Collection size/storage metrics.
</deferred>

---
*Phase: 09-admin-kb-management*
*Context gathered: 2026-03-22*
