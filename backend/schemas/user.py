"""
User schema (for profile responses).
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    role: str = "admin"
