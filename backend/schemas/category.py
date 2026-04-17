"""
Category schemas.
"""

from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    description: str = ""
    icon: str = "fa-solid fa-tag"
    status: str = "active"  # active | hidden


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    status: Optional[str] = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    status: str
    product_count: int = 0
