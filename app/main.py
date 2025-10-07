from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import face
import uvicorn
app = FastAPI(title="Face Verification API")


# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],# React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include face verification routes
app.include_router(face.router, prefix="/face", tags=["Face Recognition"])

@app.get("/")
def root():
    return {"message": "Face Verification API is running"}

