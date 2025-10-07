# face.py
from fastapi import APIRouter, UploadFile, File , Form
from app.services.face_service import verify_faces
from app.services.make_embade import get_face_embedding
from app.services.save_embedding import save_embedding
from app.services.one_to_n import one_to_n
from app.services.one_to_one import one_to_one
router = APIRouter(tags=["face"])  # remove prefix

@router.post("/verify")
async def face_verify(img1: UploadFile = File(...), img2: UploadFile = File(...)):
    result = await verify_faces(img1, img2)
    return result

@router.post("/one-one")
async def one_one(img1: UploadFile = File(...), img2: UploadFile = File(...)):
    result = await one_to_one(img1, img2)
    return result

@router.post("/save-embed")
async def save_embed(img1: UploadFile = File(...), file_path: str = Form(...),name: str = Form(...)):
    result = await get_face_embedding(img1)
    await  save_embedding(result,file_path,name)
    return {"message": "Embedding saved successfully"}


@router.post("/one-to-n")
async def one_to_n_route(img1: UploadFile = File(...)):
    result = await one_to_n(img1)
    return result

