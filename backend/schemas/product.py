"""
Product schemas — create, update, response.
"""

from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    sku: str
    category: str
    price: float
    stock: int = 0
    status: str = "active"  # active | inactive


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    status: Optional[str] = None


class ProductResponse(BaseModel):
    id: str
    name: str
    sku: str
    category: str
    price: float
    stock: int
    status: str
