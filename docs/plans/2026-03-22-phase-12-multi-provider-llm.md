# Phase 12: Multi-Provider LLM Routing

**Goal:** Refactor hardcoded OpenAI calls to use an Adapter Pattern enabling Gemini and Anthropic selection.

## Tasks
1. Implement `LLMAdapter` interface inside `src/llm/adapters.py`.
2. Implement specific adapters for OpenAI (`gpt-4o`), Gemini (`gemini-1.5-pro`), and Anthropic (`claude-3-opus`).
3. Endpoint `/admin/models` exposing unified models index dynamically per valid provider.
4. Modify Chatbot creation endpoint to validate any dynamic model string.
