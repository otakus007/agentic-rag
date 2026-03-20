# Phase 1: Core Scaffold & LangGraph Hello World - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary
Setup Poetry, FastAPI, basic LiteLLM integration, and a "Hello World" LangGraph state machine with memory persistence (PostgresSaver).
</domain>

<decisions>
## Implementation Decisions

### API Response Format
- Blocking JSON initially for Phase 1 to simplify TDD. (Streaming will be added in a later phase).

### Initial LLM Model
- Use `gpt-4o-mini` or `gemini-1.5-flash` via LiteLLM for the Phase 1 scaffolding test.

### Database Configuration
- Use Docker Postgres immediately, as PostgresSaver is heavily optimized for actual PostgreSQL and connection pooling.

### Claude's Discretion
- Code architecture for `src/` layout (e.g., separating API routers, agent state definitions).
- Connection pool initialization specifics inside FastAPI lifespan.
</decisions>

<canonical_refs>
## Canonical References
**Downstream agents MUST read these before planning or implementing.**
### Architecture
- `docs/plans/2026-03-20-agentic-rag-design.md` — Detailed system component flow.
- `.planning/research/SUMMARY.md` — Core technology stack selections.
</canonical_refs>

<code_context>
## Existing Code Insights
### Reusable Assets
- None (greenfield project initialization).
</code_context>

<specifics>
## Specific Ideas
- Use Test-Driven Development (TDD) as defined in `/writing-plans` format for the actual plan generation.
</specifics>

<deferred>
## Deferred Ideas
- Streaming SSE responses (moved to a future API refinement phase).
</deferred>

---
*Phase: 01-core-scaffold*
*Context gathered: 2026-03-20*
