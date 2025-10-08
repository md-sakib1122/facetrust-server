

from deepface import DeepFace
import numpy as np
from PIL import Image
import io
import cv2

detector_backend = 'retinaface'
model_name = 'ArcFace'

async def verify_faces(img1, img2):
    # Read bytes directly from UploadFile
    img1_bytes = await img1.read()
    img2_bytes = await img2.read()

    # Convert to NumPy arrays
    # img1_array = np.array(Image.open(io.BytesIO(img1_bytes)))
    # img2_array = np.array(Image.open(io.BytesIO(img2_bytes)))

    img1_array = cv2.imdecode(np.frombuffer(img1_bytes, np.uint8), cv2.IMREAD_COLOR)
    img2_array = cv2.imdecode(np.frombuffer(img2_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Convert BGR (OpenCV default) to RGB (DeepFace expects RGB)
    img1_array = cv2.cvtColor(img1_array, cv2.COLOR_BGR2RGB)
    img2_array = cv2.cvtColor(img2_array, cv2.COLOR_BGR2RGB)

    img1_array = cv2.resize(img1_array, (224, 224))
    img2_array = cv2.resize(img2_array, (224, 224))

    # Pass arrays directly (no saving to disk)
    result = DeepFace.verify(
        img1_array,
        img2_array,
        model_name=model_name,
        detector_backend=detector_backend,
        align=True
    )

    distance = result.get("distance", 0)
    threshold = result.get("threshold", 1)
    confidence = max(0, 1 - (distance / threshold)) * 100

    return {
        "verified": result["verified"],
        "distance": distance,
        "threshold": threshold,
        "confidence": round(confidence, 2)
    }
