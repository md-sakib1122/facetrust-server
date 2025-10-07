from fastapi import APIRouter, UploadFile, File, HTTPException
import numpy as np
import json
import os
import cv2
from app.core.model_loader import face_model  # your preloaded InsightFace model

router = APIRouter()

EMBEDDINGS_FILE = "data/face_embeddings.json"


def load_embeddings():
    if not os.path.exists(EMBEDDINGS_FILE):
        return []
    with open(EMBEDDINGS_FILE, "r") as f:
        return json.load(f)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


async def one_to_n(img1):
    try:
        img_bytes = await img1.read()
        np_img = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        faces = face_model.get(img)
        if not faces:
            raise HTTPException(status_code=400, detail="No human face detected")

        # Extract embedding and convert to float32 for performance
        embedding = faces[0].embedding.astype(np.float32)

        # Load stored embeddings
        data = load_embeddings()
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

        threshold = 0.6  # typical for ArcFace / InsightFace

        if best_score < threshold:
            return {"match": False, "score": float(best_score)}

        return {
            "match": True,
            "user_id": best_match.get("user_id"),
            "name": best_match.get("name"),
            "score": float(best_score),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
