---
phase: "04"
phase_name: "full-multi-tenant-rag-flow"
nyquist_compliant: true
validated_at: "2026-03-21"
---

# Phase 4: Full Multi-Tenant RAG Flow — Validation Strategy

## Test Infrastructure

| Framework | Config | Run Command |
|-----------|--------|-------------|
| pytest | `pyproject.toml` | `PYTHONPATH=$PWD poetry run pytest -v` |

## Per-Task Validation Map

### Task 1: Qdrant Retriever Module

| Requirement | Test | Status |
|---|---|---|
| `retrieve_context()` searches `kb_{agent_id}` | `test_retriever.py::test_retrieve_context_returns_results` | ✅ |
| Returns dicts with content, block_type, page_number, score | `test_retriever.py::test_retrieve_context_returns_results` | ✅ |
| Graceful empty list when collection missing | `test_retriever.py::test_retrieve_context_empty_when_no_collection` | ✅ |

### Task 2: Qdrant Retrieval in chatbot_node

| Requirement | Test | Status |
|---|---|---|
| `chatbot_node` calls `retrieve_context()` | `test_agent.py::test_qdrant_retrieval_injected_into_messages` | ✅ |
| Chunks injected as SystemMessage with `[1]` markers | `test_agent.py::test_qdrant_retrieval_injected_into_messages` | ✅ |
| Mem0 and Qdrant as separate SystemMessages | `test_agent.py::test_mem0_search_called_and_injected_as_system_message` + above | ✅ |
| `AgentState` includes `sources` field | `test_agent.py::test_agent_state_has_sources_field` | ✅ |

### Task 3: /chat Endpoint

| Requirement | Test | Status |
|---|---|---|
| `POST /chat` accepts message, user_id, agent_id | `test_api.py::test_chat_endpoint_returns_answer_and_sources` | ✅ |
| Returns `{answer, sources}` | `test_api.py::test_chat_endpoint_returns_answer_and_sources` | ✅ |
| Sources include content, page_number, block_type | `test_api.py::test_chat_endpoint_returns_answer_and_sources` | ✅ |
| Works with empty sources | `test_api.py::test_chat_endpoint_empty_sources` | ✅ |

## Manual-Only

None — all requirements have automated verification.

## Validation Audit 2026-03-21

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

## Sign-Off

Phase 4 is **Nyquist-compliant**. All requirements have automated test coverage.
