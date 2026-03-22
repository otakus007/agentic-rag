# v1.2 Requirements: Production Polish

## Real-time UX
- [ ] Dark/light mode toggle with system preference detection
- [ ] SSE streaming for chat responses (token-by-token display)
- [ ] Ingestion progress tracking via SSE (upload → parsing → embedding status)

## Multi-Provider LLM
- [ ] Unified LLM adapter interface (OpenAI, Gemini, Anthropic)
- [ ] Dynamic model discovery from provider APIs
- [ ] Model routing: chatbot config selects provider + model
- [ ] Provider API key management (admin-configured)

## Access Control
- [ ] User management: list, create, deactivate users
- [ ] Role-based access: admin vs. user roles
- [ ] Admin-only routes protected by role check (not just auth)
- [ ] Microsoft OAuth provider (complement existing Google)

## Admin Enhancements
- [ ] Document-level CRUD: view, search, and delete individual chunks within a KB
- [ ] KB usage analytics: query count, most-retrieved docs

## Technical Requirements
- [ ] Backend SSE endpoint for streaming chat
- [ ] Frontend SSE client with progressive text rendering
- [ ] Database migration system (Alembic or manual versioned SQL)
- [ ] API versioning strategy (v1 prefix)

## Out of Scope (v1.2)
- Multi-tenant isolation (v2.0)
- Custom system prompts per chatbot (v1.3)
- SaaS billing / subscription management
