# face.py
from fastapi import APIRouter, UploadFile, File , Form
from app.services.face_service import verify_faces
from app.services.make_embade import get_face_embedding
from app.services.save_embedding import save_embedding
from app.services.one_to_n import one_to_n
from app.services.one_to_one import one_to_one
from app.services.delete_embedding_by_id import delete_embedding_by_id;
from fastapi import APIRouter, HTTPException
from app.core.databse import db


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
async def save_embed(img1: UploadFile = File(...), file_path: str = Form(...),name: str = Form(...),notes: str = Form(...)):
    result = await get_face_embedding(img1)
    await  save_embedding(result,file_path,name,notes)
    return {"message": "Embedding saved successfully"}


@router.post("/one-to-n")
async def one_to_n_route(img1: UploadFile = File(...)):
    result = await one_to_n(img1)
    return result



@router.delete("/{user_id}")
async def delete_embedding(user_id: str):
    deleted = await delete_embedding_by_id(user_id)
    if deleted:
        return {"success": True, "message": f"Embedding with ID '{user_id}' deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"No embedding found with ID '{user_id}'")




@router.get("/embeddings")
async def get_all_embeddings():
    try:
        cursor = db.embeddings.find(
            {}, {"_id": 0, "id": 1, "image_path": 1, "notes": 1}
        )
        data = await cursor.to_list(length=None)

        if not data:
            raise HTTPException(status_code=404, detail="No embeddings found")

        return {"count": len(data), "embeddings": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
