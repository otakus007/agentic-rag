---
phase: "03"
phase_name: "document-ingestion-pipeline"
nyquist_compliant: true
validated_at: "2026-03-21"
---

# Phase 3: Document Ingestion Pipeline — Validation Strategy

## Test Infrastructure

| Framework | Config | Run Command |
|-----------|--------|-------------|
| pytest | `pyproject.toml` | `PYTHONPATH=$PWD poetry run pytest -v` |

## Per-Task Validation Map

### Task 1: Install Dependencies & Create Module Structure

| Requirement | Test File | Status |
|---|---|---|
| `qdrant-client` installed | Module imports at collection | ✅ COVERED |
| `src/ingestion/` importable | `test_ingestion.py::test_ingestion_module_imports` | ✅ COVERED |

### Task 2: MinerU PDF Parser Wrapper

| Requirement | Test File | Status |
|---|---|---|
| `parse_pdf()` returns blocks with `content`, `block_type`, `page_number` | `test_ingestion.py::test_parse_pdf_returns_normalized_blocks` | ✅ COVERED |
| Empty blocks are filtered out | `test_ingestion.py::test_parse_pdf_filters_empty_blocks` | ✅ COVERED |

### Task 3: Qdrant Embedding & Upserter

| Requirement | Test File | Status |
|---|---|---|
| `embed_and_upsert()` calls Qdrant upsert | `test_ingestion.py::test_embed_and_upsert_calls_qdrant` | ✅ COVERED |
| Collection auto-created for agent_id | `test_ingestion.py::test_embed_and_upsert_calls_qdrant` | ✅ COVERED |
| Payload contains content, block_type, page_number, agent_id | `test_ingestion.py::test_embed_and_upsert_payload_contains_metadata` | ✅ COVERED |

### Task 4: FastAPI Upload Endpoint with BackgroundTasks

| Requirement | Test File | Status |
|---|---|---|
| `POST /ingest` returns 202 | `test_api.py::test_ingest_endpoint_returns_202` | ✅ COVERED |
| Response includes `ingestion_started` status | `test_api.py::test_ingest_endpoint_returns_202` | ✅ COVERED |
| BackgroundTasks dispatched with correct args | `test_api.py::test_ingest_endpoint_dispatches_background_task` | ✅ COVERED |

## Manual-Only

None — all requirements have automated verification.

## Validation Audit 2026-03-21

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

## Sign-Off

Phase 3 is **Nyquist-compliant**. All requirements have automated test coverage.
