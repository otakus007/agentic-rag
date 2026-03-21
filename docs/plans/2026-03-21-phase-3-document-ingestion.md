# Phase 3: Document Ingestion Pipeline - Implementation Plan

> **For Antigravity:** REQUIRED SUB-SKILL: Load `executing-plans` to implement this plan task-by-task.

**Goal:** Integrate MinerU for parsing PDFs and saving embeddings into Qdrant vector database, one collection per `agent_id`.

**Architecture:** A new `src/ingestion/` module with two components: `parser.py` (MinerU PDF→text blocks) and `embedder.py` (OpenAI embeddings→Qdrant upsert). FastAPI exposes a `/ingest` endpoint that accepts file uploads and dispatches ingestion via `BackgroundTasks`.

**Tech Stack:** Python, MinerU (`magic-pdf`), Qdrant (`qdrant-client`), OpenAI embeddings (`text-embedding-3-small`), FastAPI

---

## Verification Plan
TDD approach. Each task writes failing tests first, then implements, then verifies green.

### Task 1: Install Dependencies & Create Module Structure

**Files:**
- Modify: `pyproject.toml`
- Create: `src/ingestion/__init__.py`, `src/ingestion/parser.py`, `src/ingestion/embedder.py`

<acceptance_criteria>
- `qdrant-client` and `magic-pdf` are installed.
- `src/ingestion/` module is importable.
</acceptance_criteria>

<action>
Run `poetry add qdrant-client magic-pdf`. Create empty module files.
</action>

**Step 1: Write the failing test**
```python
# tests/test_ingestion.py
def test_ingestion_module_imports():
    from src.ingestion import parser, embedder
    assert parser is not None
    assert embedder is not None
```

**Step 2: Write minimal implementation**
Create `src/ingestion/__init__.py`, `parser.py`, `embedder.py` as empty modules.

**Step 3: Run test to verify**
`PYTHONPATH=$PWD poetry run pytest tests/test_ingestion.py -v`

**Step 4: Commit**
`git commit -m "chore(03): add ingestion module and dependencies"`

---

### Task 2: MinerU PDF Parser Wrapper

**Files:**
- Modify: `src/ingestion/parser.py`
- Test: `tests/test_ingestion.py`

<acceptance_criteria>
- `parse_pdf(file_path: str) -> list[dict]` returns a list of text blocks with metadata (type, content, page_number).
- Each block has keys: `content`, `block_type`, `page_number`.
</acceptance_criteria>

<action>
Wrap MinerU's PDF extraction API. Each extracted block is normalized into a dict with `content`, `block_type` (heading/paragraph/table), and `page_number`.
</action>

**Step 1: Write the failing test**
```python
from unittest.mock import patch, MagicMock

@patch("src.ingestion.parser.extract_pdf_blocks")
def test_parse_pdf(mock_extract):
    mock_extract.return_value = [
        {"content": "Hello world", "block_type": "paragraph", "page_number": 1}
    ]
    from src.ingestion.parser import parse_pdf
    blocks = parse_pdf("/tmp/test.pdf")
    assert len(blocks) == 1
    assert blocks[0]["content"] == "Hello world"
    assert "block_type" in blocks[0]
    assert "page_number" in blocks[0]
```

**Step 2: Write minimal implementation**
Implement `parse_pdf()` calling MinerU internals. Use a thin `extract_pdf_blocks()` wrapper for mockability.

**Step 3: Commit**
`git commit -m "feat(03): add MinerU PDF parser wrapper"`

---

### Task 3: Qdrant Embedding & Upserter

**Files:**
- Modify: `src/ingestion/embedder.py`
- Test: `tests/test_ingestion.py`

<acceptance_criteria>
- `embed_and_upsert(blocks: list[dict], agent_id: str)` embeds text blocks and upserts them into a Qdrant collection named after the `agent_id`.
- Uses `text-embedding-3-small` via OpenAI client.
- Each point includes payload: `content`, `block_type`, `page_number`, `agent_id`.
</acceptance_criteria>

<action>
Create a Qdrant client wrapper. For each block, call the OpenAI embeddings API, then upsert the vector + payload into a collection named `kb_{agent_id}`.
</action>

**Step 1: Write the failing test**
```python
@patch("src.ingestion.embedder.qdrant_client")
@patch("src.ingestion.embedder.get_embedding")
def test_embed_and_upsert(mock_embed, mock_qdrant):
    mock_embed.return_value = [0.1] * 1536
    from src.ingestion.embedder import embed_and_upsert
    blocks = [{"content": "Test", "block_type": "paragraph", "page_number": 1}]
    embed_and_upsert(blocks, agent_id="test_agent")
    mock_qdrant.upsert.assert_called_once()
```

**Step 2: Write minimal implementation**
Implement embedding call + Qdrant upsert with collection auto-creation.

**Step 3: Commit**
`git commit -m "feat(03): add Qdrant embedding and upsert logic"`

---

### Task 4: FastAPI Upload Endpoint with BackgroundTasks

**Files:**
- Modify: `src/main.py`
- Test: `tests/test_api.py`

<acceptance_criteria>
- `POST /ingest` accepts a file upload (`UploadFile`) and `agent_id` query param.
- Returns `202 Accepted` with `{"status": "ingestion_started"}` immediately.
- Dispatches `parse_pdf` → `embed_and_upsert` via `BackgroundTasks`.
</acceptance_criteria>

<action>
Add `/ingest` endpoint to `src/main.py` that saves the uploaded file to a temp path, then enqueues `run_ingestion_pipeline(file_path, agent_id)` as a background task.
</action>

**Step 1: Write the failing test**
```python
def test_ingest_endpoint_returns_202():
    import io
    response = client.post(
        "/ingest?agent_id=test_agent",
        files={"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")}
    )
    assert response.status_code == 202
    assert response.json()["status"] == "ingestion_started"
```

**Step 2: Write minimal implementation**
Add the endpoint with BackgroundTasks dispatch.

**Step 3: Commit**
`git commit -m "feat(03): add /ingest endpoint with async background ingestion"`
