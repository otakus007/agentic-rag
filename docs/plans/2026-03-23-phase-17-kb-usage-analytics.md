# Phase 17: KB Usage Analytics

**Goal:** Provide visibility into how vector collections are queried to assess model popularity and chunk retrieval success.

## Tasks
1. Introduce schema updates for `query_logs` tracking the agent, chunks retrieved, and timestamp.
2. Intercept queries passed sequentially to the Vector DB to log them into PostgreSQL.
3. Build logic for `GET /admin/kb/{agent_id}/analytics` exposing counts and recent query arrays.
