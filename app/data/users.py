from app.core.passwords import verify_password
from app.schemas.user import UserPublic
from sqlmodel import Session, select
from app.db.models import User


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = session.exec(select(User).where(User.email == email)).first()

    if user and verify_password(password, user.password_hash):
        return user

    return None


def get_user_by_id(session: Session, user_id: str) -> UserPublic | None:
    user = session.get(User, user_id)

    if user is None:
        return None

    return UserPublic(
        user_id=user.user_id,
        full_name=user.full_name,
        email=user.email,
    )
