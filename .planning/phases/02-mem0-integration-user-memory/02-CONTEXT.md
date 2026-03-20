# Phase 2: Mem0 Integration & User Memory - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary
Connect Mem0 for retrieving and storing cross-session semantic facts per `user_id`, independent of the short-term checkpoint logic.
</domain>

<decisions>
## Implementation Decisions

### Memory Isolation Model
- Partition memories by both `user_id` AND `agent_id` so each chatbot instance has distinct identity/memory.

### Context Injection Mode
- Retrieve and inject Mem0 summaries dynamically into the `SystemMessage` on every graph run.

### Extraction Strategy
- Use an explicit tool (`Save_Memory`) called by the LLM instead of passive background extraction.

### Database Architecture
- Combine Mem0 (pgvector) and PostgresSaver in the same physical database instance via shared `DATABASE_URL`.
</decisions>

<canonical_refs>
## Canonical References
**Downstream agents MUST read these before planning or implementing.**
- `docs/plans/2026-03-20-agentic-rag-design.md` — Core memory architecture diagram.
</canonical_refs>

<code_context>
## Existing Code Insights
### Reusable Assets
- `src.agent.graph` — The StateGraph builder where the Mem0 dependency will be injected.
- `src.main` — FastAPI app where the `DATABASE_URL` pool is initialized.
</code_context>

<specifics>
## Specific Ideas
- Use TDD and create a dummy pytest to ensure memory storage and retrieval works.
</specifics>

<deferred>
## Deferred Ideas
- None — discussion stayed within phase scope.
</deferred>

---
*Phase: 02-mem0-integration-user-memory*
*Context gathered: 2026-03-20*
