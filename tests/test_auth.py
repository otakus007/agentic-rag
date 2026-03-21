from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from src.auth.providers import verify_token, _detect_provider, decode_token
from src.auth.dependencies import get_current_user
import pytest


# --- Task 1: JWT Token Verification ---

@patch("src.auth.providers.decode_token")
def test_verify_token_google(mock_decode):
    mock_decode.return_value = {
        "sub": "google-uid-123",
        "email": "user@gmail.com",
        "iss": "accounts.google.com",
    }
    result = verify_token("fake-token")
    assert result["user_id"] == "google-uid-123"
    assert result["email"] == "user@gmail.com"
    assert result["provider"] == "google"


@patch("src.auth.providers.decode_token")
def test_verify_token_microsoft(mock_decode):
    mock_decode.return_value = {
        "sub": "ms-uid-456",
        "email": "user@outlook.com",
        "iss": "https://login.microsoftonline.com/tenant-id/v2.0",
    }
    result = verify_token("fake-token")
    assert result["user_id"] == "ms-uid-456"
    assert result["email"] == "user@outlook.com"
    assert result["provider"] == "microsoft"


@patch("src.auth.providers.decode_token")
def test_verify_token_unknown_issuer_raises_401(mock_decode):
    mock_decode.return_value = {
        "sub": "uid-789",
        "iss": "https://unknown-provider.com",
    }
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc_info:
        verify_token("fake-token")
    assert exc_info.value.status_code == 401


@patch("src.auth.providers.decode_token")
def test_verify_token_missing_sub_raises_401(mock_decode):
    mock_decode.return_value = {
        "email": "user@gmail.com",
        "iss": "accounts.google.com",
    }
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc_info:
        verify_token("fake-token")
    assert exc_info.value.status_code == 401


# --- Task 2: FastAPI Auth Dependency ---

def test_get_current_user_dependency():
    """Verify the auth dependency works via a test FastAPI app."""
    test_app = FastAPI()

    @test_app.get("/protected")
    def protected(user=Depends(get_current_user)):
        return {"user_id": user["user_id"]}

    client = TestClient(test_app)

    # Without token → 403 (HTTPBearer returns 403 for missing credentials)
    response = client.get("/protected")
    assert response.status_code == 401

    # With valid token (mocked)
    with patch("src.auth.providers.decode_token") as mock_decode:
        mock_decode.return_value = {
            "sub": "test-uid",
            "email": "test@test.com",
            "iss": "accounts.google.com",
        }
        response = client.get(
            "/protected",
            headers={"Authorization": "Bearer fake-jwt-token"},
        )
        assert response.status_code == 200
        assert response.json()["user_id"] == "test-uid"
