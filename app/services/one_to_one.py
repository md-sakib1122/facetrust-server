from app.core.model_loader import face_model
import numpy as np
import cv2

async def one_to_one(img1, img2):
    # Read image bytes
    img1_bytes = await img1.read()
    img2_bytes = await img2.read()
    print("data aitace ")
    # Decode bytes to OpenCV arrays
    img1_bgr = cv2.imdecode(np.frombuffer(img1_bytes, np.uint8), cv2.IMREAD_COLOR)
    img2_bgr = cv2.imdecode(np.frombuffer(img2_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Convert BGR → RGB (InsightFace expects RGB)
    img1_rgb = cv2.cvtColor(img1_bgr, cv2.COLOR_BGR2RGB)
    img2_rgb = cv2.cvtColor(img2_bgr, cv2.COLOR_BGR2RGB)

    # Detect faces
    faces1 = face_model.get(img1_rgb)
    faces2 = face_model.get(img2_rgb)

    # Handle missing or invalid faces
    if len(faces1) == 0 or len(faces2) == 0:
        return {"error": "Face not detected in one or both images"}

    # Get the first detected face embeddings
    emb1 = faces1[0].embedding
    emb2 = faces2[0].embedding

    # Compute cosine similarity
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    confidence = float(similarity * 100)

    # Define threshold (adjustable)
    threshold = 0.5
    verified = similarity > threshold

    return {
        "verified": bool(verified),
        "similarity": round(float(similarity), 4),
        "confidence": round(confidence, 2),
        "threshold": threshold
    }
