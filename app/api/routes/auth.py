from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.data.users import authenticate_user
from app.db.database import get_session
from app.schemas.auth import LoginResponse, UserLoginRequest
from app.schemas.user import UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: UserLoginRequest, session: Session = Depends(get_session)):
    user = authenticate_user(session, payload.email, payload.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    public_user = UserPublic(
        user_id=user.user_id,
        full_name=user.full_name,
        email=user.email,
    )

    return LoginResponse(
        access_token=create_access_token(user.user_id),
        token_type="bearer",
        user=public_user,
    )


@router.get("/me", response_model=UserPublic)
def me(current_user: UserPublic = Depends(get_current_user)):
    return current_user
