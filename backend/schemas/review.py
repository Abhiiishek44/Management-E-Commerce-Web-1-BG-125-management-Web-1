"""
Review schemas.
"""

from pydantic import BaseModel
from typing import Optional


class ReviewCreate(BaseModel):
    product_name: str
    customer_name: str
    rating: int  # 1-5
    comment: str = ""
    status: str = "pending"  # pending | approved | rejected


class ReviewUpdate(BaseModel):
    status: Optional[str] = None   # moderate: approve / reject
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: str
    product_name: str
    customer_name: str
    rating: int
    comment: str
    status: str
    created_at: str
