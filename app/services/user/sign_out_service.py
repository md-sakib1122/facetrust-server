from fastapi import Response

ACCESS_COOKIE_NAME = "access_token"

async def sign_out_user(response: Response):
    response.delete_cookie(
        key=ACCESS_COOKIE_NAME,
        path="/",
        samesite="lax"
    )
    return {"message": "Sign out successful"}
