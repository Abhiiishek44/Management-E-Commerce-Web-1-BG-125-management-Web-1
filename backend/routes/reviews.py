"""
Review Routes — /api/reviews
"""

from fastapi import APIRouter, Depends, Query
from controllers import review_controller
from schemas.review import ReviewCreate, ReviewUpdate
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@router.get("")
async def list_reviews(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(""),
    _user: dict = Depends(get_current_user),
):
    return await review_controller.list_reviews(page, limit, status)


@router.post("")
async def create_review(data: ReviewCreate, _user: dict = Depends(get_current_user)):
    return await review_controller.create_review(data)


@router.put("/{review_id}")
async def update_review(review_id: str, data: ReviewUpdate, _user: dict = Depends(get_current_user)):
    return await review_controller.update_review(review_id, data)


@router.delete("/{review_id}")
async def delete_review(review_id: str, _user: dict = Depends(get_current_user)):
    return await review_controller.delete_review(review_id)
