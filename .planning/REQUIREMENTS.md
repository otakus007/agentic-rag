# v1.1 Requirements: Frontend UI

## User Chat Interface
- [ ] Chat page with message input, conversation history, and streaming AI responses
- [ ] Display inline citation markers `[1]` linked to source documents
- [ ] Sources panel showing retrieved document chunks with page numbers
- [ ] Dark mode / light mode toggle
- [ ] OAuth login flow (Google/Microsoft) with token storage
- [ ] Conversation list sidebar for session management
- [ ] Responsive layout (mobile-friendly)

## Admin: Knowledge Base Management
- [ ] Dashboard showing list of knowledge bases (Qdrant collections)
- [ ] Upload PDF files to create/update a knowledge base
- [ ] View ingestion status and document count per KB
- [ ] Delete knowledge base

## Admin: Chatbot Builder
- [ ] Create chatbot with name, description, assigned KB, and LLM model selection
- [ ] List existing chatbots with status
- [ ] Edit chatbot configuration (KB assignment, model)
- [ ] Test chat panel within admin to verify chatbot behavior

## Technical Requirements
- [ ] Vue 3 + Vite + Tailwind CSS frontend scaffold
- [ ] UUPM (ui-ux-pro-max-skill) design system integration
- [ ] API client module for backend communication (`/chat`, `/ingest`, `/health`)
- [ ] JWT token management (store, refresh, attach to API calls)
- [ ] Monorepo structure: `frontend/` directory alongside existing `src/`

## Out of Scope (v1.1)
- Multi-LLM routing (v1.2)
- User management / role-based access control (v1.2)
- Real-time WebSocket streaming (use SSE or polling first)
