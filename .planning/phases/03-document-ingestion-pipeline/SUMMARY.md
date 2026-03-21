# Phase 3: Document Ingestion Pipeline - Summary

**Executed Plan:** 03-PLAN.md

## What was Built
- Created `src/ingestion/` module with `parser.py` (MinerU wrapper) and `embedder.py` (Qdrant upsert).
- Parser uses a mockable `extract_pdf_blocks()` boundary for MinerU internals; normalizes blocks with `content`, `block_type`, `page_number`.
- Embedder creates per-`agent_id` Qdrant collections (`kb_{agent_id}`), embeds via `text-embedding-3-small`, upserts with full metadata payloads.
- Added `POST /ingest` endpoint accepting PDF uploads with async `BackgroundTasks` dispatch.
- Installed `qdrant-client` and `python-multipart` dependencies.

## Self-Check: PASS — 17/17 tests green
