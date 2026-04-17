"""
Promotion Routes — /api/promotions
"""

from fastapi import APIRouter, Depends
from controllers import promotion_controller
from schemas.promotion import PromotionCreate, PromotionUpdate
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/promotions", tags=["Promotions"])


@router.get("")
async def list_promotions(_user: dict = Depends(get_current_user)):
    return await promotion_controller.list_promotions()


@router.post("")
async def create_promotion(data: PromotionCreate, _user: dict = Depends(get_current_user)):
    return await promotion_controller.create_promotion(data)


@router.put("/{promo_id}")
async def update_promotion(promo_id: str, data: PromotionUpdate, _user: dict = Depends(get_current_user)):
    return await promotion_controller.update_promotion(promo_id, data)


@router.delete("/{promo_id}")
async def delete_promotion(promo_id: str, _user: dict = Depends(get_current_user)):
    return await promotion_controller.delete_promotion(promo_id)
