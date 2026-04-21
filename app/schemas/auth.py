from pydantic import BaseModel, EmailStr
from app.schemas.user import UserPublic


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserPublic
