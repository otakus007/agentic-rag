"""Tests for src.llm.adapters — model registry and adapter interface."""
import pytest
from unittest.mock import patch, MagicMock
from src.llm.adapters import get_all_models, get_adapter, LLMAdapter, PROVIDERS, _adapters


def test_get_all_models_returns_all_providers():
    models = get_all_models()
    assert "openai" in models
    assert "gemini" in models
    assert "anthropic" in models
    assert "gpt-4o-mini" in models["openai"]
    assert "gemini-2.0-flash" in models["gemini"]
    assert "claude-sonnet-4-20250514" in models["anthropic"]


def test_get_all_models_contains_expected_count():
    models = get_all_models()
    total = sum(len(v) for v in models.values())
    assert total >= 8  # at least 3 + 3 + 2


def test_get_adapter_unknown_provider():
    with pytest.raises(ValueError, match="Unknown provider"):
        _adapters.clear()
        get_adapter("invalid_provider")


def test_llm_adapter_base_raises():
    adapter = LLMAdapter()
    with pytest.raises(NotImplementedError):
        adapter.complete([], "model")
    with pytest.raises(NotImplementedError):
        adapter.list_models()


def test_providers_registry_has_all():
    assert set(PROVIDERS.keys()) == {"openai", "gemini", "anthropic"}
