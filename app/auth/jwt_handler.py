from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))  # default 1 day

if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in .env")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token with expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict | None:
    """
    Verify a JWT token.
    Returns payload dictionary if valid, None if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except ExpiredSignatureError:
        return {"error": "Token expired"}
    except JWTError:
        return {"error": "Invalid token"}
