# Phase 16: Provider API Key Management

**Goal:** Store keys dynamically in DB using symmetric encryption instead of relying purely on static environment variables.

## Tasks
1. Write Fernet-based `src/auth/crypto.py` bound to securely provisioned `SECRET_KEY`.
2. Expose `GET /admin/api-keys` masking plain text for validated connections.
3. Allow updating encrypted keys via `PUT /admin/api-keys`.
4. Delete keys fully restricting access via `DELETE /admin/api-keys/{provider}`.
