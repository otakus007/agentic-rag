import io
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from langchain_core.messages import AIMessage, HumanMessage
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("src.main.AsyncConnectionPool")
def test_lifespan_initializes_pool(mock_pool_cls):
    mock_pool = AsyncMock()
    mock_pool_cls.return_value = mock_pool
    
    with TestClient(app) as tc:
        response = tc.get("/health")
        assert response.status_code == 200
    
    mock_pool_cls.assert_called_once()
    mock_pool.open.assert_awaited_once()
    mock_pool.close.assert_awaited_once()

@patch("src.main.run_ingestion_pipeline")
def test_ingest_endpoint_returns_202(mock_pipeline):
    response = client.post(
        "/ingest?agent_id=test_agent",
        files={"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 fake content"), "application/pdf")}
    )
    assert response.status_code == 202
    assert response.json()["status"] == "ingestion_started"
    assert response.json()["filename"] == "test.pdf"

@patch("src.main.run_ingestion_pipeline")
def test_ingest_endpoint_dispatches_background_task(mock_pipeline):
    client.post(
        "/ingest?agent_id=my_agent",
        files={"file": ("doc.pdf", io.BytesIO(b"%PDF-1.4 test"), "application/pdf")}
    )
    mock_pipeline.assert_called_once()
    call_args = mock_pipeline.call_args[0]
    assert call_args[1] == "my_agent"
    assert call_args[0].endswith(".pdf")

# --- Phase 4: /chat endpoint tests ---

@patch("src.agent.graph.app_graph")
def test_chat_endpoint_returns_answer_and_sources(mock_graph):
    """Verify /chat returns structured {answer, sources} response."""
    mock_graph.invoke.return_value = {
        "messages": [
            HumanMessage(content="hi"),
            AIMessage(content="Hello! Based on [1], the answer is yes.")
        ],
        "sources": [
            {"content": "The answer is yes.", "page_number": 1, "block_type": "paragraph", "score": 0.95}
        ]
    }
    
    response = client.post("/chat", json={
        "message": "hi",
        "user_id": "u1",
        "agent_id": "a1"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert data["answer"] == "Hello! Based on [1], the answer is yes."
    assert len(data["sources"]) == 1
    assert data["sources"][0]["content"] == "The answer is yes."

@patch("src.agent.graph.app_graph")
def test_chat_endpoint_empty_sources(mock_graph):
    """Verify /chat works when no documents are retrieved."""
    mock_graph.invoke.return_value = {
        "messages": [
            HumanMessage(content="hello"),
            AIMessage(content="Hi there!")
        ],
        "sources": []
    }
    
    response = client.post("/chat", json={
        "message": "hello",
        "user_id": "u1",
        "agent_id": "a1"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Hi there!"
    assert data["sources"] == []
