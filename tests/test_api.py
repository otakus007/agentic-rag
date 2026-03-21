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
