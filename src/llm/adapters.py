"""
Unified LLM Adapter Interface.

Provides a consistent API across OpenAI, Google Gemini, and Anthropic providers.
Each provider implements the `complete(messages, model)` method.
"""
import os
from typing import List, Dict, Optional


class LLMAdapter:
    """Base class for LLM provider adapters."""

    def complete(self, messages: List[Dict], model: str) -> str:
        raise NotImplementedError

    def list_models(self) -> List[str]:
        raise NotImplementedError


class OpenAIAdapter(LLMAdapter):
    """OpenAI API adapter (gpt-4o, gpt-4o-mini, gpt-3.5-turbo)."""

    MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]

    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def complete(self, messages: List[Dict], model: str = "gpt-4o-mini") -> str:
        response = self.client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content or ""

    def list_models(self) -> List[str]:
        return self.MODELS


class GeminiAdapter(LLMAdapter):
    """Google Gemini API adapter."""

    MODELS = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-pro"]

    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
        self._genai = genai

    def complete(self, messages: List[Dict], model: str = "gemini-2.0-flash") -> str:
        gen_model = self._genai.GenerativeModel(model)
        # Convert OpenAI-style messages to Gemini format
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        response = gen_model.generate_content(prompt)
        return response.text or ""

    def list_models(self) -> List[str]:
        return self.MODELS


class AnthropicAdapter(LLMAdapter):
    """Anthropic Claude API adapter."""

    MODELS = ["claude-sonnet-4-20250514", "claude-3-5-haiku-20241022"]

    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def complete(self, messages: List[Dict], model: str = "claude-sonnet-4-20250514") -> str:
        # Separate system message if present
        system = ""
        chat_msgs = []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                chat_msgs.append(m)

        response = self.client.messages.create(
            model=model,
            max_tokens=4096,
            system=system or "You are a helpful assistant.",
            messages=chat_msgs,
        )
        return response.content[0].text

    def list_models(self) -> List[str]:
        return self.MODELS


# Provider registry
PROVIDERS = {
    "openai": OpenAIAdapter,
    "gemini": GeminiAdapter,
    "anthropic": AnthropicAdapter,
}

_adapters: Dict[str, LLMAdapter] = {}


def get_adapter(provider: str) -> LLMAdapter:
    """Get or create a cached adapter instance for the given provider."""
    if provider not in _adapters:
        if provider not in PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(PROVIDERS.keys())}")
        _adapters[provider] = PROVIDERS[provider]()
    return _adapters[provider]


def get_all_models() -> Dict[str, List[str]]:
    """Return all available models grouped by provider."""
    return {
        "openai": OpenAIAdapter.MODELS,
        "gemini": GeminiAdapter.MODELS,
        "anthropic": AnthropicAdapter.MODELS,
    }
