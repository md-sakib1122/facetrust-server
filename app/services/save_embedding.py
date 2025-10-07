import json
import os

EMBEDDINGS_FILE = "data/face_embeddings.json"
os.makedirs("data", exist_ok=True)

async def save_embedding(embedding: list[float], image_path: str, name: str):
    # Load existing data if file exists
    data = []
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, "r") as f:
            data = json.load(f)

    # Append new entry
    data.append({
        "embedding": embedding,
        "image_path": image_path,
        "name": name
    })

    # Save back to file
    with open(EMBEDDINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)
