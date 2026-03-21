# Phase 5: OAuth & API Gateways - Implementation Plan

> **For Antigravity:** REQUIRED SUB-SKILL: Load `executing-plans` to implement this plan task-by-task.

**Goal:** Add Microsoft/Google SSO middleware to FastAPI. Associate `user_id` tokens with API requests to enforce multi-tenancy.

**Architecture:** A new `src/auth/` module with `providers.py` (Google/Microsoft JWT verification) and `dependencies.py` (FastAPI `Security` dependency extracting `user_id` from Bearer tokens). Protected endpoints derive `user_id` from the token instead of the request body.

---

## Verification Plan
TDD with mocked JWT tokens. `PYTHONPATH=$PWD poetry run pytest -v` must pass after each task.

### Task 1: JWT Token Verification Module

**Files:**
- Create: `src/auth/__init__.py`, `src/auth/providers.py`
- Modify: `pyproject.toml`
- Test: `tests/test_auth.py`

<acceptance_criteria>
- `python-jose[cryptography]` and `httpx` are installed.
- `verify_google_token(token: str) -> dict` returns decoded claims with `sub`, `email`.
- `verify_microsoft_token(token: str) -> dict` returns decoded claims with `sub`, `email`.
- `verify_token(token: str) -> dict` auto-detects provider and returns unified `{"user_id": sub, "email": ..., "provider": ...}`.
- Invalid tokens raise `HTTPException(401)`.
</acceptance_criteria>

**Step 1: Write the failing test**
```python
# tests/test_auth.py
from unittest.mock import patch, MagicMock
from src.auth.providers import verify_token

@patch("src.auth.providers.jwt.decode")
def test_verify_token_google(mock_decode):
    mock_decode.return_value = {"sub": "google-uid-123", "email": "user@gmail.com", "iss": "accounts.google.com"}
    result = verify_token("fake-token")
    assert result["user_id"] == "google-uid-123"
    assert result["provider"] == "google"

@patch("src.auth.providers.jwt.decode")
def test_verify_token_microsoft(mock_decode):
    mock_decode.return_value = {"sub": "ms-uid-456", "email": "user@outlook.com", "iss": "https://login.microsoftonline.com"}
    result = verify_token("fake-token")
    assert result["user_id"] == "ms-uid-456"
    assert result["provider"] == "microsoft"
```

**Step 2: Write minimal implementation**
Implement JWT decoding with issuer-based provider detection.

**Step 3: Commit**
`git commit -m "feat(05): add JWT token verification module"`

---

### Task 2: FastAPI Auth Dependency

**Files:**
- Create: `src/auth/dependencies.py`
- Test: `tests/test_auth.py`

<acceptance_criteria>
- `get_current_user(token: str = Security(HTTPBearer()))` extracts Bearer token and calls `verify_token()`.
- Returns a `UserInfo` dict with `user_id`, `email`, `provider`.
- Missing/invalid tokens return 401 with `{"detail": "Invalid authentication credentials"}`.
</acceptance_criteria>

**Step 1: Write the failing test**
```python
@patch("src.auth.dependencies.verify_token")
def test_get_current_user(mock_verify):
    mock_verify.return_value = {"user_id": "uid-1", "email": "a@b.com", "provider": "google"}
    from src.auth.dependencies import get_current_user
    # Test via FastAPI TestClient with Authorization header
```

**Step 2: Write minimal implementation**

**Step 3: Commit**
`git commit -m "feat(05): add FastAPI auth dependency"`

---

### Task 3: Protect Endpoints with Auth

**Files:**
- Modify: `src/main.py`
- Test: `tests/test_api.py`

<acceptance_criteria>
- `/health` remains public (no auth).
- `/chat` requires Bearer token; `user_id` comes from token, not request body.
- `/ingest` requires Bearer token; `user_id` from token.
- Requests without tokens to protected endpoints return 401/403.
</acceptance_criteria>

**Step 1: Write the failing test**
```python
def test_chat_requires_auth():
    response = client.post("/chat", json={"message": "hi", "agent_id": "a1"})
    assert response.status_code in [401, 403]

@patch("src.auth.dependencies.verify_token")
def test_chat_with_valid_token(mock_verify):
    mock_verify.return_value = {"user_id": "uid-1", "email": "a@b.com", "provider": "google"}
    response = client.post("/chat", json={"message": "hi", "agent_id": "a1"},
                          headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
```

**Step 2: Write minimal implementation**
Add `Depends(get_current_user)` to `/chat` and `/ingest` endpoints. Remove `user_id` from `ChatRequest` body.

**Step 3: Commit**
`git commit -m "feat(05): protect /chat and /ingest with auth"`
