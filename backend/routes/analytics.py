"""
Analytics Routes — /api/analytics
"""

from fastapi import APIRouter, Depends
from controllers import analytics_controller
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/overview")
async def get_overview(_user: dict = Depends(get_current_user)):
    return await analytics_controller.get_overview()


@router.get("/traffic")
async def get_traffic(_user: dict = Depends(get_current_user)):
    return await analytics_controller.get_traffic()


@router.get("/devices")
async def get_devices(_user: dict = Depends(get_current_user)):
    return await analytics_controller.get_devices()
