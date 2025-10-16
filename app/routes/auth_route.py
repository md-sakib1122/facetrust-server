from fastapi import APIRouter, HTTPException, Response,Depends
from app.models.userModel import UserModel
from app.services.user.user_service import create_user
from app.models.signInModel import SignInModel
from app.services.user.sign_in_service import sign_in_user
from app.utils.role_guard import get_current_user
router = APIRouter(tags=["auth"])

@router.post("/signup")
async def add_group(user: UserModel):
    try:
        user_id = await create_user(user.model_dump())
        return {"message": "User created successfully", "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/signin")
async def sign_in(data: SignInModel, response: Response):
    print("hit korche",data)
    try:
        result = await sign_in_user(data.model_dump(),response)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["user_id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

