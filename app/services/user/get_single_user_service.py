from typing import Optional, Any, Dict
from bson import ObjectId
from app.core.databse import db  # your Motor database instance

async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a single user document from MongoDB by its ObjectId string,
    and manually transforms the document for JSON compatibility.
    """

    object_id = ObjectId(user_id)
    collection = db["users"]

    # ✅ await the async find_one
    user_document = await collection.find_one({"_id": object_id})

    if user_document:
        user_document["id"] = str(user_document["_id"])
        user_document.pop("_id")
        return user_document

    return None
