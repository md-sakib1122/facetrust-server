from datetime import datetime
from app.core.databse import db
from app.auth.password_utils import hash_password
async def create_user(data: dict):
    collection = db["users"]
    hashed_pw = hash_password(data["password"])
    document = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_pw,
        "role": data["role"],
        "parent": data["parent"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    result = await collection.insert_one(document)
    return str(result.inserted_id)
