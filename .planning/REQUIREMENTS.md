# v1.3 Requirements: Admin Polish

## Provider API Key Management
- [ ] Admin settings page for managing LLM provider API keys
- [ ] Secure storage of API keys in database (encrypted at rest)
- [ ] Per-provider key status indicator (valid/invalid/missing)
- [ ] Frontend form to add/update/delete keys per provider

## KB Usage Analytics
- [ ] Track query count per knowledge base
- [ ] Track most-retrieved document chunks
- [ ] Analytics dashboard widget on admin KB detail page
- [ ] Query log table in PostgreSQL

## Custom System Prompts
- [ ] System prompt field on chatbot create/edit form
- [ ] Store system prompt in chatbots table
- [ ] Pass system prompt to LLM adapter during chat invocation
- [ ] Default system prompt template for new chatbots

## Technical Requirements
- [ ] Database migration: add columns (system_prompt to chatbots, api_keys table, query_logs table)
- [ ] Frontend admin settings route and view
- [ ] API key encryption/decryption utility

## Out of Scope (v1.3)
- Microsoft OAuth provider (v1.4)
- Ingestion SSE progress tracking (v1.4)
- Multi-tenant isolation (v2.0)
