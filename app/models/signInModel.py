from pydantic import BaseModel, EmailStr
class SignInModel(BaseModel):
    email: EmailStr
    password: str