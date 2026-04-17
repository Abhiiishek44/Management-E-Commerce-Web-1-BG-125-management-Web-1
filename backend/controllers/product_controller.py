"""
Product Controller — Full CRUD with search and pagination.
"""

import math
from fastapi import HTTPException
from config.database import get_database
from utils.helpers import to_object_id, serialize_doc, serialize_docs
from schemas.product import ProductCreate, ProductUpdate


async def list_products(page: int, limit: int, search: str) -> dict:
    db = get_database()
    query = {}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"sku": {"$regex": search, "$options": "i"}},
        ]

    total = await db.products.count_documents(query)
    skip = (page - 1) * limit
    cursor = db.products.find(query).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)

    return {
        "success": True,
        "data": serialize_docs(products),
        "total": total,
        "page": page,
        "limit": limit,
        "pages": math.ceil(total / limit) if limit else 0,
    }


async def get_product(product_id: str) -> dict:
    db = get_database()
    doc = await db.products.find_one({"_id": to_object_id(product_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found.")
    return {"success": True, "data": serialize_doc(doc)}


async def create_product(data: ProductCreate) -> dict:
    db = get_database()
    product_doc = data.model_dump()
    result = await db.products.insert_one(product_doc)
    product_doc["id"] = str(result.inserted_id)
    product_doc.pop("_id", None)
    return {"success": True, "message": "Product created.", "data": product_doc}


async def update_product(product_id: str, data: ProductUpdate) -> dict:
    db = get_database()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")

    result = await db.products.update_one(
        {"_id": to_object_id(product_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found.")

    doc = await db.products.find_one({"_id": to_object_id(product_id)})
    return {"success": True, "message": "Product updated.", "data": serialize_doc(doc)}


async def delete_product(product_id: str) -> dict:
    db = get_database()
    result = await db.products.delete_one({"_id": to_object_id(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found.")
    return {"success": True, "message": "Product deleted."}
