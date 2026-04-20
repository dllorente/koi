from fastapi import Depends, HTTPException, status

#from app.data.users import get_user_by_id, parse_mock_token
from app.core.security import decode_access_token, get_bearer_token
from app.data.users import get_user_by_id
from app.schemas.user import UserPublic
from sqlmodel import Session
from app.db.database import get_session

def get_current_user(
    token: str = Depends(get_bearer_token),
    session: Session = Depends(get_session),
) -> UserPublic:
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user