"""FastAPI authentication dependency.

Extracts Bearer token from the Authorization header and verifies it,
returning a UserInfo dict with user_id, email, and provider.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.providers import verify_token
from typing import Dict, Any

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """FastAPI dependency that extracts and verifies the Bearer token.
    
    Returns:
        {"user_id": str, "email": str, "provider": str}
    
    Raises:
        HTTPException(401/403) if token is missing or invalid.
    """
    return verify_token(credentials.credentials)
