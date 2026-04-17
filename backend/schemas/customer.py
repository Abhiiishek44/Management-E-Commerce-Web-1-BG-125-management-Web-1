"""
Customer schemas.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str = ""
    total_orders: int = 0
    total_spent: float = 0.0
    status: str = "active"  # active | inactive


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[str] = None


class CustomerResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    total_orders: int
    total_spent: float
    status: str
