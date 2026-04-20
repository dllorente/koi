from pydantic import BaseModel, EmailStr

class UserPublic(BaseModel):
    user_id: str
    full_name: str
    email: EmailStr

