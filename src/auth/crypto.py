"""API key encryption/decryption utility.

Uses Fernet symmetric encryption for storing provider API keys at rest.
The encryption key is derived from the app's SECRET_KEY environment variable.
"""
import os
import base64
import hashlib


def _get_fernet_key() -> bytes:
    """Derive a Fernet key from SECRET_KEY env var."""
    secret = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    # Fernet requires 32 url-safe base64 encoded bytes
    key = hashlib.sha256(secret.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_key(api_key: str) -> str:
    """Encrypt an API key for database storage."""
    from cryptography.fernet import Fernet
    f = Fernet(_get_fernet_key())
    return f.encrypt(api_key.encode()).decode()


def decrypt_key(encrypted: str) -> str:
    """Decrypt an API key from database storage."""
    from cryptography.fernet import Fernet
    f = Fernet(_get_fernet_key())
    return f.decrypt(encrypted.encode()).decode()


def mask_key(api_key: str) -> str:
    """Mask an API key for display: show first 4 and last 4 chars."""
    if len(api_key) <= 8:
        return "****"
    return api_key[:4] + "…" + api_key[-4:]
