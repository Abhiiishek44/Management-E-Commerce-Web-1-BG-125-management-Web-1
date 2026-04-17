"""
Auth Routes — /api/auth
"""

from fastapi import APIRouter, Depends, Request, Response, HTTPException
from jose import JWTError

from schemas.auth import RegisterRequest, LoginRequest
from controllers import auth_controller
from middleware.auth import get_current_user
from utils.security import decode_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register")
async def register(data: RegisterRequest):
    return await auth_controller.register(data)


@router.post("/login")
async def login(data: LoginRequest, response: Response):
    return await auth_controller.login(data, response)


@router.post("/refresh")
async def refresh(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing.")
    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token.")
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type.")
    return await auth_controller.refresh(payload["sub"])


@router.post("/logout")
async def logout(response: Response):
    return await auth_controller.logout(response)


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return await auth_controller.me(current_user)
