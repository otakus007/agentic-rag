# Phase 4: Full Multi-Tenant RAG Flow - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary
Connect LangGraph to query Qdrant based on Mem0 injected history. Output proper citations.
</domain>

<decisions>
## Implementation Decisions

### Retrieval Integration Point
- Automatic pre-processing: search Qdrant with the user query before the LLM call.
- Inject retrieved document chunks as additional SystemMessage context alongside the Mem0 memories.
- Mirrors the existing Mem0 injection pattern in `chatbot_node`.

### Citation Format
- Inline `[1]` markers in the LLM response text.
- Structured `sources` array in the response JSON: `{"answer": "...[1]", "sources": [{"content": "...", "page": 3, "file": "policy.pdf"}]}`.
- Gives the frontend flexibility to render citations however it chooses.

### Retrieval Scope
- Search Qdrant using only the latest user message (not combined with Mem0 context).
- Mem0 context is already injected separately — combining would dilute the search query.
- The LLM sees both contexts and synthesizes them naturally.
</decisions>

<canonical_refs>
## Canonical References
**Downstream agents MUST read these before planning or implementing.**
- `docs/plans/2026-03-20-agentic-rag-design.md` — Core architecture with RAG retrieval flow.
- `src/agent/graph.py` — Current chatbot_node with Mem0 injection pattern to replicate for Qdrant.
- `src/ingestion/embedder.py` — Qdrant client factory and collection naming convention (`kb_{agent_id}`).
</canonical_refs>

<code_context>
## Existing Code Insights
### Reusable Assets
- `src/agent/graph.py::chatbot_node` — Mem0 pre-processing pattern to replicate for Qdrant retrieval.
- `src/ingestion/embedder.py::get_qdrant_client()` — Qdrant client factory to reuse for queries.
- `src/ingestion/embedder.py::get_embedding()` — Embedding function to reuse for query vectorization.
- `src/agent/state.py::AgentState` — Already has `user_id` and `agent_id` for scoping retrieval.
</code_context>

<specifics>
## Specific Ideas
- Create `src/agent/retriever.py` with a `retrieve_context(query, agent_id)` function.
- Add citation instruction to the system prompt so the LLM formats `[1]` markers.
- Structure the `/chat` response to include both `answer` and `sources` fields.
</specifics>

<deferred>
## Deferred Ideas
- Re-ranking retrieved results with a cross-encoder (future optimization).
- Hybrid search combining dense + sparse vectors (future optimization).
</deferred>

---
*Phase: 04-full-multi-tenant-rag-flow*
*Context gathered: 2026-03-21*
