# Phase 11: SSE Streaming Chat

**Goal:** Replace synchronous `/chat` endpoint with SSE Streaming implementation for token-by-token generation.

## Tasks
1. Backend `/chat/stream` endpoint emitting server-sent events using `StreamingResponse`.
2. Frontend `useChat.js` rewritten using `fetch` streams over SSE to parse tokens.
3. Light/Dark mode reactive toggle via `useTheme.js` modifying `data-theme`.
