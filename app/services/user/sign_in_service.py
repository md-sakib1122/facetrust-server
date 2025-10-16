from app.auth.password_utils import verify_password

from app.core.databse import db
from fastapi import Response
from passlib.context import CryptContext
from app.auth.jwt_handler import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_COOKIE_NAME = "access_token"


async def sign_in_user(data: dict, response: Response):
    user = await db.users.find_one({"email": data["email"]})
    if not user:
        return {"message": "User Does not Exist", "id": None}

    # verify hashed password
    if not verify_password(data["password"], user["password"]):
        return {"message": "Invalid Password", "id": None}

    # generate access token
    payload = {"user_id": str(user["_id"]), "email": user["email"], "role": user["role"]}
    access_token = create_access_token(payload)  # set expiry in jwt_handler

    # set access token in HttpOnly cookie
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,       # prevents JS access
        secure=False,
        path="/", # True in production with HTTPS
        samesite="lax",      # adjust if needed
        max_age=24 * 3600    # 1 day in seconds
    )

    # optionally return user info
    return {
        "message": "Sign in successful",
        "id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"]
    }

