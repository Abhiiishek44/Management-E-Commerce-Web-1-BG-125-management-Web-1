"""
Staff schemas.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class StaffCreate(BaseModel):
    name: str
    email: EmailStr
    role: str = "staff"  # admin | manager | staff
    status: str = "active"  # active | inactive


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    status: Optional[str] = None


class StaffResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    status: str
