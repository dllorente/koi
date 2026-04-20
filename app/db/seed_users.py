from sqlmodel import Session, select

from app.db.models import User


def seed_users(session: Session) -> None:
    demo_users = [
        User(
            user_id="u001",
            full_name="David Llorente Raposo",
            email="davidllorenten@example.com",
            password_hash="$argon2id$v=19$m=65536,t=3,p=4$y27Qf6z8x8kA69OZ+8Ha7w$LfwNq+fcUNxon3qdAtgMTdg/IzTOqr0OLBfqLFem7Hc",
        ),
        User(
            user_id="u002",
            full_name="Fernanda Morales Barba",
            email="ferMor@example.com",
            password_hash="$argon2id$v=19$m=65536,t=3,p=4$walDvSW2xtU6/kUD5O0Zag$a/PhW4tqS0hizJEaoQrSu6cnk0ncoIZM6qTetFNQmOU",
        ),
        User(
            user_id="u003",
            full_name="Carlos Pérez Ruiz",
            email="carlos.perez@example.com",
            password_hash="$argon2id$v=19$m=65536,t=3,p=4$etL2p/2lK5g0VRygTKAmvg$NKtmQE3KU+HAQoBksScva7sBVP+Sh/HYNOl4tSAPCk8",
        ),
    ]

    for demo_user in demo_users:
        existing_user = session.get(User, demo_user.user_id)

        if existing_user is not None:
            continue

        existing_email = session.exec(
            select(User).where(User.email == demo_user.email)
        ).first()

        if existing_email is not None:
            continue

        session.add(demo_user)

    session.commit()