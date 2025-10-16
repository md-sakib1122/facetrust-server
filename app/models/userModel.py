from pydantic import BaseModel, EmailStr
from typing import Optional

class UserModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    parent: Optional[str] = None

