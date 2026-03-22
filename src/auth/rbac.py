"""Role-based access control middleware.

Adds `require_admin` dependency that checks user role from JWT claims.
Uses the users table in PostgreSQL to store role assignments.
"""
from fastapi import Depends, HTTPException, Request
from src.auth.dependencies import get_current_user
from typing import Dict, Any


async def get_user_role(request: Request, user: dict = Depends(get_current_user)) -> Dict[str, Any]:
    """Enrich user dict with role from database. Defaults to 'user' if not found."""
    pool = request.state.pool
    async with pool.connection() as conn:
        row = await conn.execute(
            "SELECT role FROM users WHERE user_id = %s", (user["user_id"],)
        )
        result = await row.fetchone()
        user["role"] = result[0] if result else "user"
    return user


async def require_admin(user: dict = Depends(get_user_role)) -> Dict[str, Any]:
    """Dependency that requires the user to have admin role."""
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
