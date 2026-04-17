"""
Settings Routes — /api/settings
"""

from fastapi import APIRouter, Depends
from controllers import settings_controller
from schemas.settings import SettingsUpdate
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("")
async def get_settings(_user: dict = Depends(get_current_user)):
    return await settings_controller.get_settings()


@router.put("")
async def update_settings(data: SettingsUpdate, _user: dict = Depends(get_current_user)):
    return await settings_controller.update_settings(data)
