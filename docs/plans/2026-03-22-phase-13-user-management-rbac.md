# Phase 13: User Management & RBAC

**Goal:** Introduce formal admin vs user roles, modifying JWT to securely encode privileges.

## Tasks
1. Add `users` table via simple lifespan script migrations.
2. Build `src/auth/rbac.py` defining a `require_admin` FastAPI dependency.
3. Manage users through `GET /admin/users`.
4. Allow elevating user to Admin through `PUT /admin/users/{user_id}/role`.
