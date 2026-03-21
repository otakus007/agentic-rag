import io
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("src.main.AsyncConnectionPool")
def test_lifespan_initializes_pool(mock_pool_cls):
    """Verify that the lifespan context manager creates and opens the pool."""
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
    """Verify /ingest accepts a file upload and returns 202."""
    response = client.post(
        "/ingest?agent_id=test_agent",
        files={"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 fake content"), "application/pdf")}
    )
    assert response.status_code == 202
    assert response.json()["status"] == "ingestion_started"
    assert response.json()["filename"] == "test.pdf"

@patch("src.main.run_ingestion_pipeline")
def test_ingest_endpoint_dispatches_background_task(mock_pipeline):
    """Verify the background task is dispatched with correct arguments."""
    client.post(
        "/ingest?agent_id=my_agent",
        files={"file": ("doc.pdf", io.BytesIO(b"%PDF-1.4 test"), "application/pdf")}
    )
    mock_pipeline.assert_called_once()
    call_args = mock_pipeline.call_args[0]
    assert call_args[1] == "my_agent"  # agent_id
    assert call_args[0].endswith(".pdf")  # temp file path
