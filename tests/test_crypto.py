"""Tests for src.auth.crypto — API key encryption utilities."""
import os
import pytest
from src.auth.crypto import encrypt_key, decrypt_key, mask_key


def test_encrypt_decrypt_roundtrip():
    original = "sk-test-1234567890abcdef"
    encrypted = encrypt_key(original)
    assert encrypted != original
    decrypted = decrypt_key(encrypted)
    assert decrypted == original


def test_encrypt_produces_different_ciphertexts():
    """Due to Fernet IV, same input produces different ciphertext each time."""
    a = encrypt_key("test-key")
    b = encrypt_key("test-key")
    # Both should decrypt to same value but ciphertext differs
    assert decrypt_key(a) == decrypt_key(b) == "test-key"


def test_mask_key_short():
    assert mask_key("abcd") == "****"


def test_mask_key_normal():
    masked = mask_key("sk-1234567890abcdef")
    assert masked.startswith("sk-1")
    assert masked.endswith("cdef")
    assert "…" in masked
