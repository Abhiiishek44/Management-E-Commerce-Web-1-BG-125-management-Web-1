"""
Category Controller — Full CRUD with product count.
"""

from fastapi import HTTPException
from config.database import get_database
from utils.helpers import to_object_id, serialize_doc, serialize_docs
from schemas.category import CategoryCreate, CategoryUpdate


async def list_categories() -> dict:
    db = get_database()
    cursor = db.categories.find()
    categories = await cursor.to_list(length=100)
    result = []
    for cat in categories:
        cat_data = serialize_doc(cat)
        count = await db.products.count_documents({"category": cat_data["name"]})
        cat_data["product_count"] = count
        result.append(cat_data)
    return {"success": True, "data": result}


async def create_category(data: CategoryCreate) -> dict:
    db = get_database()
    doc = data.model_dump()
    result = await db.categories.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    doc["product_count"] = 0
    return {"success": True, "message": "Category created.", "data": doc}


async def update_category(cat_id: str, data: CategoryUpdate) -> dict:
    db = get_database()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")
    result = await db.categories.update_one(
        {"_id": to_object_id(cat_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found.")
    doc = await db.categories.find_one({"_id": to_object_id(cat_id)})
    cat_data = serialize_doc(doc)
    cat_data["product_count"] = await db.products.count_documents({"category": cat_data["name"]})
    return {"success": True, "message": "Category updated.", "data": cat_data}


async def delete_category(cat_id: str) -> dict:
    db = get_database()
    result = await db.categories.delete_one({"_id": to_object_id(cat_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found.")
    return {"success": True, "message": "Category deleted."}
