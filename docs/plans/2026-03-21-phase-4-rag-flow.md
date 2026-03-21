# Phase 4: Full Multi-Tenant RAG Flow - Implementation Plan

> **For Antigravity:** REQUIRED SUB-SKILL: Load `executing-plans` to implement this plan task-by-task.

**Goal:** Connect LangGraph to query Qdrant based on user input and output LLM responses with inline citations and a structured `sources` array.

**Architecture:** A new `src/agent/retriever.py` module wraps Qdrant semantic search, reusing `get_qdrant_client()` and `get_embedding()` from Phase 3. The `chatbot_node` is extended to inject Qdrant document chunks as a second SystemMessage alongside Mem0 memories. A new `/chat` endpoint returns `{"answer": "...[1]", "sources": [...]}`.

---

## Verification Plan
TDD approach. `PYTHONPATH=$PWD poetry run pytest -v` must pass after each task.

### Task 1: Create Qdrant Retriever Module

**Files:**
- Create: `src/agent/retriever.py`
- Test: `tests/test_retriever.py`

<acceptance_criteria>
- `retrieve_context(query: str, agent_id: str) -> list[dict]` searches the `kb_{agent_id}` collection.
- Returns a list of dicts with `content`, `block_type`, `page_number`, `score`.
- Gracefully returns empty list if collection doesn't exist.
</acceptance_criteria>

<action>
Create `src/agent/retriever.py`. Import `get_qdrant_client` and `get_embedding` from `src.ingestion.embedder`. Embed the query, search Qdrant, return top-k results with payload + score.
</action>

**Step 1: Write the failing test**
```python
# tests/test_retriever.py
from unittest.mock import patch, MagicMock
from src.agent.retriever import retrieve_context

@patch("src.agent.retriever.get_qdrant_client")
@patch("src.agent.retriever.get_embedding")
def test_retrieve_context(mock_embed, mock_qdrant_factory):
    mock_embed.return_value = [0.1] * 1536
    mock_qdrant = MagicMock()
    mock_qdrant.search.return_value = [
        MagicMock(payload={"content": "Policy doc", "page_number": 2, "block_type": "paragraph"}, score=0.9)
    ]
    mock_qdrant_factory.return_value = mock_qdrant
    results = retrieve_context("what is the policy?", agent_id="agent_1")
    assert len(results) == 1
    assert results[0]["content"] == "Policy doc"
    assert results[0]["score"] == 0.9
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(04): add Qdrant retriever module"`

---

### Task 2: Integrate Qdrant Retrieval into chatbot_node

**Files:**
- Modify: `src/agent/graph.py`
- Test: `tests/test_agent.py`

<acceptance_criteria>
- `chatbot_node` calls `retrieve_context()` with the user message and `agent_id`.
- Retrieved chunks are injected as a SystemMessage with citation numbering.
- Citation instruction is added to the system prompt so the LLM uses `[1]` markers.
- Mem0 memories and Qdrant documents appear as separate SystemMessages.
</acceptance_criteria>

<action>
In `chatbot_node`, after the Mem0 injection block, add a Qdrant retrieval block. Format each retrieved chunk as a numbered source and inject as a SystemMessage. Add a citation instruction SystemMessage.
</action>

**Step 1: Write the failing test**
```python
@patch("src.agent.graph.retrieve_context")
@patch("src.agent.graph.get_mem0_client")
@patch("src.agent.graph.llm")
def test_qdrant_retrieval_injected(mock_llm, mock_mem0, mock_retriever):
    mock_llm.invoke.return_value = AIMessage(content="Based on [1]...")
    mock_mem0_client = MagicMock()
    mock_mem0_client.search.return_value = {"results": []}
    mock_mem0.return_value = mock_mem0_client
    mock_retriever.return_value = [
        {"content": "Policy text", "page_number": 2, "block_type": "paragraph", "score": 0.9}
    ]
    result = app_graph.invoke({...})
    mock_retriever.assert_called_once()
    # Verify LLM received system message with document context
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(04): integrate Qdrant retrieval with citation prompting"`

---

### Task 3: Add /chat Endpoint with Citation Response

**Files:**
- Modify: `src/main.py`
- Test: `tests/test_api.py`

<acceptance_criteria>
- `POST /chat` accepts `{"message": str, "user_id": str, "agent_id": str}`.
- Returns `{"answer": str, "sources": list[dict]}`.
- Sources include `content`, `page_number`, `block_type`.
</acceptance_criteria>

<action>
Add a `/chat` endpoint that invokes the graph, extracts the AI response and collected sources, and returns the structured citation response.
</action>

**Step 1: Write the failing test**
```python
@patch("src.main.app_graph")
def test_chat_endpoint(mock_graph):
    mock_graph.invoke.return_value = {
        "messages": [..., AIMessage(content="Answer [1]")],
        "sources": [{"content": "Doc", "page_number": 1}]
    }
    response = client.post("/chat", json={"message": "hi", "user_id": "u1", "agent_id": "a1"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "sources" in response.json()
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(04): add /chat endpoint with citation response"`
