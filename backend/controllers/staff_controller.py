"""
Staff Controller — Full CRUD.
"""

from fastapi import HTTPException
from config.database import get_database
from utils.helpers import to_object_id, serialize_doc, serialize_docs
from schemas.staff import StaffCreate, StaffUpdate


async def list_staff() -> dict:
    db = get_database()
    cursor = db.staff.find()
    members = await cursor.to_list(length=100)
    return {"success": True, "data": serialize_docs(members)}


async def create_staff(data: StaffCreate) -> dict:
    db = get_database()
    doc = data.model_dump()
    result = await db.staff.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return {"success": True, "message": "Staff member added.", "data": doc}


async def update_staff(staff_id: str, data: StaffUpdate) -> dict:
    db = get_database()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")
    result = await db.staff.update_one(
        {"_id": to_object_id(staff_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Staff member not found.")
    doc = await db.staff.find_one({"_id": to_object_id(staff_id)})
    return {"success": True, "message": "Staff member updated.", "data": serialize_doc(doc)}


async def delete_staff(staff_id: str) -> dict:
    db = get_database()
    result = await db.staff.delete_one({"_id": to_object_id(staff_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Staff member not found.")
    return {"success": True, "message": "Staff member removed."}
