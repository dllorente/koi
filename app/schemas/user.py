from pydantic import BaseModel, EmailStr

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    user_id: str
    full_name: str
    email: EmailStr

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserPublic