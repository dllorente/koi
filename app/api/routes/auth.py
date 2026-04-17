from fastapi import APIRouter, HTTPException, status, Depends

from app.core.security import authenticate_user, create_mock_token
from app.schemas.user import LoginResponse, UserLoginRequest, UserPublic
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(payload: UserLoginRequest):
    user = authenticate_user(payload.email, payload.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    public_user = UserPublic(
        user_id=user["user_id"],
        full_name=user["full_name"],
        email=user["email"],
    )

    return LoginResponse(
        access_token=create_mock_token(user["user_id"]),
        token_type="bearer",
        user=public_user,
    )

@router.get("/me", response_model=UserPublic)
def read_me(current_user: UserPublic = Depends(get_current_user)):
    return current_user