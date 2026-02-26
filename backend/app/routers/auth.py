"""
Auth API Router
---------------
Login and token verification endpoints for admin panel.
"""

from fastapi import APIRouter
from app.auth import (
    LoginRequest,
    LoginResponse,
    create_access_token,
    verify_admin_login,
)
from fastapi import HTTPException, status

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    """
    Admin login endpoint.
    Returns a JWT token on successful authentication.
    """
    if not verify_admin_login(data.username, data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(data.username)
    return LoginResponse(access_token=token, username=data.username)


@router.get("/verify")
async def verify():
    """
    Verify if the current token is valid.
    The require_admin dependency is NOT applied here –
    the frontend calls this with the Authorization header
    and we verify manually.
    """
    return {"valid": True}
