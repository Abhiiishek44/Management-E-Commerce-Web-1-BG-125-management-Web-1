"""
ForgeAdmin Backend — Common Helpers
"""

from bson import ObjectId


def to_object_id(id_str: str) -> ObjectId:
    """Convert a string to a BSON ObjectId. Raises ValueError if invalid."""
    if not ObjectId.is_valid(id_str):
        raise ValueError(f"Invalid ObjectId: {id_str}")
    return ObjectId(id_str)


def serialize_doc(doc: dict) -> dict:
    """Convert a MongoDB document to a JSON-serializable dict.
    Converts ObjectId _id to string field 'id'."""
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id"))
    return doc


def serialize_docs(docs: list[dict]) -> list[dict]:
    """Serialize a list of MongoDB documents."""
    return [serialize_doc(d) for d in docs]
