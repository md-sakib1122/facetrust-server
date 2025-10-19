import datetime
from app.core.databse import db

async def save_tracking(emp_id: str, match_score: str):
    collection = db["tracks"]

    document = {
        "emp_id": emp_id,
        "match_score": match_score,
        "timestamp": datetime.datetime.now()
    }
    result = await collection.insert_one(document)
    return str(result.inserted_id)


