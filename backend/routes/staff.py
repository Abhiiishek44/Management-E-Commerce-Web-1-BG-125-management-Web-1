"""
Staff Routes — /api/staff
"""

from fastapi import APIRouter, Depends
from controllers import staff_controller
from schemas.staff import StaffCreate, StaffUpdate
from middleware.auth import get_current_user

router = APIRouter(prefix="/api/staff", tags=["Staff"])


@router.get("")
async def list_staff(_user: dict = Depends(get_current_user)):
    return await staff_controller.list_staff()


@router.post("")
async def create_staff(data: StaffCreate, _user: dict = Depends(get_current_user)):
    return await staff_controller.create_staff(data)


@router.put("/{staff_id}")
async def update_staff(staff_id: str, data: StaffUpdate, _user: dict = Depends(get_current_user)):
    return await staff_controller.update_staff(staff_id, data)


@router.delete("/{staff_id}")
async def delete_staff(staff_id: str, _user: dict = Depends(get_current_user)):
    return await staff_controller.delete_staff(staff_id)
