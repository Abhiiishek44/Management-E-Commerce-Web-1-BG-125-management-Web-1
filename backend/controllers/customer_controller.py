"""
Customer Controller — Full CRUD with search and pagination.
"""

import math
from fastapi import HTTPException
from config.database import get_database
from utils.helpers import to_object_id, serialize_doc, serialize_docs
from schemas.customer import CustomerCreate, CustomerUpdate


async def list_customers(page: int, limit: int, search: str) -> dict:
    db = get_database()
    query = {}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
        ]
    total = await db.customers.count_documents(query)
    skip = (page - 1) * limit
    cursor = db.customers.find(query).skip(skip).limit(limit)
    customers = await cursor.to_list(length=limit)
    return {
        "success": True,
        "data": serialize_docs(customers),
        "total": total,
        "page": page,
        "limit": limit,
        "pages": math.ceil(total / limit) if limit else 0,
    }


async def get_customer(customer_id: str) -> dict:
    db = get_database()
    doc = await db.customers.find_one({"_id": to_object_id(customer_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return {"success": True, "data": serialize_doc(doc)}


async def create_customer(data: CustomerCreate) -> dict:
    db = get_database()
    doc = data.model_dump()
    result = await db.customers.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return {"success": True, "message": "Customer created.", "data": doc}


async def update_customer(customer_id: str, data: CustomerUpdate) -> dict:
    db = get_database()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")
    result = await db.customers.update_one(
        {"_id": to_object_id(customer_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found.")
    doc = await db.customers.find_one({"_id": to_object_id(customer_id)})
    return {"success": True, "message": "Customer updated.", "data": serialize_doc(doc)}


async def delete_customer(customer_id: str) -> dict:
    db = get_database()
    result = await db.customers.delete_one({"_id": to_object_id(customer_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return {"success": True, "message": "Customer deleted."}
