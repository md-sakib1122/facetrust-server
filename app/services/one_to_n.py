from fastapi import APIRouter, UploadFile, HTTPException
import numpy as np
import cv2
from app.core.model_loader import face_model  # your preloaded InsightFace model
from app.core.databse import db  # MongoDB client

router = APIRouter()


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


async def one_to_n(img1: UploadFile,company_id: str):
    try:
        print("company_id",company_id)
        # Read image bytes
        img_bytes = await img1.read()
        np_img = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Detect face and get embedding
        faces = face_model.get(img)
        if not faces:
            raise HTTPException(status_code=400, detail="No human face detected")

        embedding = faces[0].embedding.astype(np.float32)

        # Fetch embeddings from MongoDB
        cursor = db.embeddings.find(
           {"company_id": company_id}, {"id": 1, "embedding": 1, "image_path": 1, "notes": 1}
        )
        data = await cursor.to_list(length=None)

        if not data:
            raise HTTPException(status_code=404, detail="No embeddings in database")

        best_match = None
        best_score = -1

        for row in data:
            db_emb = np.array(row["embedding"], dtype=np.float32)
            score = cosine_similarity(embedding, db_emb)
            if score > best_score:
                best_score = score
                best_match = row

        threshold = 0.6  # typical for InsightFace
        if best_score < threshold:
            return {"match": False, "score": float(best_score)}

        return {
            "match": True,
            "user_id": best_match.get("id"),
            "image_path": best_match.get("image_path"),
            "notes": best_match.get("notes"),
            "score": float(best_score),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
