# Phase 5: OAuth & API Gateways - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary
Add Microsoft/Google SSO middleware to FastAPI. Associate `user_id` tokens with API requests to enforce multi-tenancy.
</domain>

<decisions>
## Implementation Decisions

### SSO Provider Scope
- Support both Microsoft (Azure AD) and Google OAuth2 simultaneously.
- Use `authlib` or `python-jose` + HTTPX for token validation.
- No email/password fallback — SSO-only for minimal auth surface.

### Token-to-User Mapping
- Use the SSO provider's `sub` (subject) claim as `user_id`.
- Stable, unique per provider, won't change on email updates.
- Optional `users` table for display info mapping (deferred).

### Endpoint Protection Strategy
- `/health` stays public (no auth required).
- `/chat` and `/ingest` require valid Bearer token.
- No admin roles — any authenticated user can ingest into their own `agent_id` namespace.
- Admin role separation deferred to a future phase.
</decisions>

<canonical_refs>
## Canonical References
**Downstream agents MUST read these before planning or implementing.**
- `src/main.py` — FastAPI app where auth middleware/dependencies will be added.
- `src/agent/state.py` — AgentState with `user_id` field that auth will populate.
</canonical_refs>

<code_context>
## Existing Code Insights
### Reusable Assets
- `src/main.py` — Current endpoints already accept `user_id` in request bodies; auth will replace manual user_id with token-derived identity.
- FastAPI `Depends()` pattern for injecting auth dependencies into endpoints.
### Integration Points
- `/chat` endpoint — `ChatRequest.user_id` will be populated from JWT token instead of request body.
- `/ingest` endpoint — `agent_id` query param stays; user identity from token.
</code_context>

<specifics>
## Specific Ideas
- Create `src/auth/` module with `dependencies.py` (FastAPI auth dependency) and `providers.py` (Google/Microsoft token verification).
- Use FastAPI `Security` dependency to extract and validate Bearer tokens.
- TDD with mocked JWT tokens to verify auth flow without live OAuth providers.
</specifics>

<deferred>
## Deferred Ideas
- Admin roles and permission levels for `/ingest` vs `/chat`.
- `users` table for profile/display info persistence.
- API key auth as an alternative to OAuth (for programmatic access).
</deferred>

---
*Phase: 05-oauth-api-gateways*
*Context gathered: 2026-03-21*
