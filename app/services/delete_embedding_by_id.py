# app/core/save_embedding.py
from app.core.databse import db


async def delete_embedding_by_id(user_id: str) -> bool:
    """
    Delete an embedding document from the 'embeddings' collection by user ID.

    Args:
        user_id (str): The 'id' of the embedding document to delete.

    Returns:
        bool: True if a document was deleted, False otherwise.
    """
    collection = db["embeddings"]
    result = await collection.delete_one({"id": user_id})
    return result.deleted_count > 0
