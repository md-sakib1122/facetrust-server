# app/utils/role_guard.py
from fastapi import Depends, HTTPException, status, Request
from app.auth.jwt_handler import verify_token

# JWT verification dependency
def get_current_user(request: Request):
    token = request.cookies.get("access_token")  # from HttpOnly cookie
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    payload = verify_token(token)
    if not payload or "error" in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=payload.get("error", "Invalid token"))
    print("this is payload",payload)
    return payload

# Role-based dependency
def require_role(role: str):
    def role_checker(user=Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Forbidden: requires {role} role")
        return user
    return role_checker
