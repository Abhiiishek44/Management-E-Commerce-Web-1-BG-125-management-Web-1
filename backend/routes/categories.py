"""
Category Routes — /api/categories
"""

from fastapi import APIRouter, Depends
from controllers import category_controller
from schemas.category import CategoryCreate, CategoryUpdate
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("")
async def list_categories(_user: dict = Depends(get_current_user)):
    return await category_controller.list_categories()


@router.post("")
async def create_category(data: CategoryCreate, _user: dict = Depends(get_current_user)):
    return await category_controller.create_category(data)


@router.put("/{cat_id}")
async def update_category(cat_id: str, data: CategoryUpdate, _user: dict = Depends(get_current_user)):
    return await category_controller.update_category(cat_id, data)


@router.delete("/{cat_id}")
async def delete_category(cat_id: str, _user: dict = Depends(get_current_user)):
    return await category_controller.delete_category(cat_id)
