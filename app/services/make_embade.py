# server/app/service/face_service.py
from app.core.model_loader import face_model
import cv2
import numpy as np


async def get_face_embedding(img1):
    img_bytes = await img1.read()
    img_array = np.frombuffer(img_bytes, np.uint8)
    img_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    faces = face_model.get(img_rgb)
    if len(faces) == 0:
        return None
    return faces[0].embedding.tolist()
