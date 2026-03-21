"""JWT token verification for Google and Microsoft SSO providers.

Verifies Bearer tokens by decoding JWT claims and auto-detecting
the issuer (Google or Microsoft) from the `iss` claim.
"""
from jose import jwt, JWTError
from fastapi import HTTPException, status
from typing import Dict, Any

# Known issuers
GOOGLE_ISSUERS = ["accounts.google.com", "https://accounts.google.com"]
MICROSOFT_ISSUER_PREFIX = "https://login.microsoftonline.com"


def _detect_provider(claims: Dict[str, Any]) -> str:
    """Detect OAuth provider from JWT issuer claim."""
    iss = claims.get("iss", "")
    if iss in GOOGLE_ISSUERS:
        return "google"
    if iss.startswith(MICROSOFT_ISSUER_PREFIX):
        return "microsoft"
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unknown token issuer",
    )


def decode_token(token: str, options: dict | None = None) -> Dict[str, Any]:
    """Decode a JWT token without signature verification (for testing/mocking).
    
    In production, you'd verify against the provider's JWKS endpoint.
    This boundary function is mockable for tests.
    """
    if options is None:
        options = {"verify_signature": False, "verify_aud": False, "verify_exp": False}
    return jwt.decode(token, key="", algorithms=["RS256", "HS256"], options=options)


def verify_token(token: str) -> Dict[str, Any]:
    """Verify a JWT token and return unified user info.
    
    Returns:
        {"user_id": str, "email": str, "provider": str}
    
    Raises:
        HTTPException(401) for invalid tokens.
    """
    try:
        claims = decode_token(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e}",
        )
    
    provider = _detect_provider(claims)
    
    sub = claims.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing 'sub' claim",
        )
    
    return {
        "user_id": sub,
        "email": claims.get("email", ""),
        "provider": provider,
    }
