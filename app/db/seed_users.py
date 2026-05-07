from sqlmodel import Session, select
from app.db.models import User
from app.data.users import DEMO_USERS


def seed_users(session: Session) -> None:
    for demo in DEMO_USERS:
        # Evitar duplicados por user_id
        existing = session.exec(
            select(User).where(User.user_id == demo["user_id"])
        ).first()
        if existing:
            continue

        # Evitar duplicados por email (por si cambias ids en el futuro)
        existing_email = session.exec(
            select(User).where(User.email == demo["email"])
        ).first()
        if existing_email:
            continue

        user = User(
            user_id=demo["user_id"],
            full_name=demo["full_name"],
            email=demo["email"],
            password_hash=demo["password_hash"],
        )
        session.add(user)

    session.commit()
