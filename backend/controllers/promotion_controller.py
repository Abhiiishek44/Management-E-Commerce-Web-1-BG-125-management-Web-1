"""
Promotion Controller — Full CRUD.
"""

from fastapi import HTTPException
from config.database import get_database
from utils.helpers import to_object_id, serialize_doc, serialize_docs
from schemas.promotion import PromotionCreate, PromotionUpdate


async def list_promotions() -> dict:
    db = get_database()
    cursor = db.promotions.find()
    promotions = await cursor.to_list(length=100)
    return {"success": True, "data": serialize_docs(promotions)}


async def create_promotion(data: PromotionCreate) -> dict:
    db = get_database()
    doc = data.model_dump()
    result = await db.promotions.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return {"success": True, "message": "Promotion created.", "data": doc}


async def update_promotion(promo_id: str, data: PromotionUpdate) -> dict:
    db = get_database()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")
    result = await db.promotions.update_one(
        {"_id": to_object_id(promo_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Promotion not found.")
    doc = await db.promotions.find_one({"_id": to_object_id(promo_id)})
    return {"success": True, "message": "Promotion updated.", "data": serialize_doc(doc)}


async def delete_promotion(promo_id: str) -> dict:
    db = get_database()
    result = await db.promotions.delete_one({"_id": to_object_id(promo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Promotion not found.")
    return {"success": True, "message": "Promotion deleted."}
