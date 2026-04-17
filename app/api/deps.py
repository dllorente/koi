from fastapi import Header, HTTPException, status

from app.core.security import get_user_by_id, parse_mock_token
from app.schemas.user import UserPublic

def get_current_user(authorization: str | None = Header(default=None)) -> UserPublic:
    if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
            )

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme",
        )

    user_id = parse_mock_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return UserPublic(
        user_id=user["user_id"],
        full_name=user["full_name"],
        email=user["email"],
    )