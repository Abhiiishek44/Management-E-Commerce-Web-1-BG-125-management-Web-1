"""
Auth Controller — Registration, Login, Token Refresh, Logout, Me.
All business logic is handled directly here.
"""

from fastapi import Response, HTTPException, status
from bson import ObjectId

from config.database import get_database
from schemas.auth import RegisterRequest, LoginRequest
from utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


async def register(data: RegisterRequest) -> dict:
    db = get_database()

    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered.")

    user_doc = {
        "full_name": data.full_name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": "admin",
    }
    result = await db.users.insert_one(user_doc)

    return {
        "success": True,
        "message": "Registration successful.",
        "data": {
            "id": str(result.inserted_id),
            "full_name": data.full_name,
            "email": data.email,
            "role": "admin",
        },
    }


async def login(data: LoginRequest, response: Response) -> dict:
    db = get_database()

    user = await db.users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    user_id = str(user["_id"])
    access_token = create_access_token({"sub": user_id})
    refresh_token = create_refresh_token({"sub": user_id})

    # Set refresh token in HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Set True in production with HTTPS
        samesite="lax",
        max_age=7 * 24 * 60 * 60,  # 7 days
        path="/",
    )

    return {
        "success": True,
        "message": "Login successful.",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user.get("role", "admin"),
            },
        },
    }


async def refresh(user_id: str) -> dict:
    db = get_database()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    access_token = create_access_token({"sub": user_id})
    return {
        "success": True,
        "message": "Token refreshed.",
        "data": {"access_token": access_token, "token_type": "bearer"},
    }


async def logout(response: Response) -> dict:
    response.delete_cookie("refresh_token", path="/")
    return {"success": True, "message": "Logged out successfully."}


async def me(current_user: dict) -> dict:
    return {"success": True, "data": current_user}
