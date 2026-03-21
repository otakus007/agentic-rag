# Phase 3: Document Ingestion Pipeline - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary
Integrate MinerU for parsing PDFs and saving embeddings into Qdrant vector database.
</domain>

<decisions>
## Implementation Decisions

### Document Format Scope
- PDF-only via MinerU for Phase 3. Other formats (DOCX, HTML, plain text) deferred to a future phase.

### Chunking & Embedding Strategy
- Use MinerU's native block-level structure (headings, paragraphs, tables) for chunking.
- Embed with `text-embedding-3-small` via LiteLLM/OpenAI for cost-efficiency.

### Qdrant Collection Architecture
- One Qdrant collection per `agent_id`. Each chatbot gets its own isolated vector space matching the "each chatbot has its own knowledge base" requirement.

### Ingestion Trigger
- Async background job via FastAPI `BackgroundTasks`. User uploads a file, gets an immediate acknowledgment response, and ingestion runs asynchronously.
</decisions>

<canonical_refs>
## Canonical References
**Downstream agents MUST read these before planning or implementing.**
- `docs/plans/2026-03-20-agentic-rag-design.md` — Core architecture with MinerU + Qdrant flow.
</canonical_refs>

<code_context>
## Existing Code Insights
### Reusable Assets
- `src/main.py` — FastAPI app where the upload endpoint and `BackgroundTasks` will be added.
- `src/agent/memory.py` — Pattern for `DATABASE_URL`-based config initialization (reuse for Qdrant client setup).
- `src/agent/graph.py` — Graph builder that Phase 4 will connect to Qdrant retrieval.
</code_context>

<specifics>
## Specific Ideas
- Create `src/ingestion/` module with `parser.py` (MinerU wrapper) and `embedder.py` (Qdrant upsert logic).
- Use TDD with mocked file uploads and mocked Qdrant client to verify the pipeline.
</specifics>

<deferred>
## Deferred Ideas
- DOCX/HTML/plain text format support (future phase).
- Real-time ingestion progress tracking via WebSockets (future phase).
</deferred>

---
*Phase: 03-document-ingestion-pipeline*
*Context gathered: 2026-03-21*
