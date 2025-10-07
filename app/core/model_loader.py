# server/app/core/model_loader.py
import insightface

print("Loading InsightFace model...")

face_model = insightface.app.FaceAnalysis()
face_model.prepare(ctx_id=-1)  # -1 = CPU, 0 = GPU

print("Model loaded successfully.")
