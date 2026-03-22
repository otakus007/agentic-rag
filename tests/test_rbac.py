"""Tests for RBAC middleware and user management endpoints."""
import pytest
from src.auth.rbac import require_admin, get_user_role


def test_require_admin_exists():
    """Verify require_admin function is importable."""
    assert callable(require_admin)


def test_get_user_role_exists():
    """Verify get_user_role function is importable."""
    assert callable(get_user_role)
