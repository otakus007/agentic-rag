# Phase 14: Document CRUD

**Goal:** Permit admins to visualize, explore, and delete atomic text chunks within a Knowledge Base.

## Tasks
1. Enable chunk listing inside Qdrant: `GET /admin/kb/{agent_id}/documents`.
2. Implement atomic deletion on vector index level: `DELETE /admin/kb/{agent_id}/documents/{doc_id}`.
