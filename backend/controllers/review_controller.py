"""
Review Controller — Full CRUD with status filtering.
"""

import math
from datetime import datetime, timezone
from fastapi import HTTPException
from config.database import get_database
from utils.helpers import to_object_id, serialize_doc, serialize_docs
from schemas.review import ReviewCreate, ReviewUpdate


async def list_reviews(page: int, limit: int, status: str) -> dict:
    db = get_database()
    query = {}
    if status:
        query["status"] = status
    total = await db.reviews.count_documents(query)
    skip = (page - 1) * limit
    cursor = db.reviews.find(query).sort("created_at", -1).skip(skip).limit(limit)
    reviews = await cursor.to_list(length=limit)
    return {
        "success": True,
        "data": serialize_docs(reviews),
        "total": total,
        "page": page,
        "limit": limit,
        "pages": math.ceil(total / limit) if limit else 0,
    }


async def create_review(data: ReviewCreate) -> dict:
    db = get_database()
    doc = data.model_dump()
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    result = await db.reviews.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return {"success": True, "message": "Review created.", "data": doc}


async def update_review(review_id: str, data: ReviewUpdate) -> dict:
    db = get_database()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")
    result = await db.reviews.update_one(
        {"_id": to_object_id(review_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review not found.")
    doc = await db.reviews.find_one({"_id": to_object_id(review_id)})
    return {"success": True, "message": "Review updated.", "data": serialize_doc(doc)}


async def delete_review(review_id: str) -> dict:
    db = get_database()
    result = await db.reviews.delete_one({"_id": to_object_id(review_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found.")
    return {"success": True, "message": "Review deleted."}
