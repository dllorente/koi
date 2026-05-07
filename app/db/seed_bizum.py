from sqlmodel import select
from app.db.models import BizumEvent, User  # ajusta import según tu estructura
from app.data.bizum import DEMO_BIZUM
from sqlmodel import Session


def seed_bizum(session: Session) -> None:
    for demo in DEMO_BIZUM:
        # Evitar duplicados por bizum_id
        existing = session.exec(
            select(BizumEvent).where(BizumEvent.bizum_id == demo["bizum_id"])
        ).first()
        if existing:
            continue

        # Asegurar que el usuario existe
        user_exists = session.exec(
            select(User).where(User.user_id == demo["user_id"])
        ).first()
        if not user_exists:
            continue

        event = BizumEvent(
            bizum_id=demo["bizum_id"],
            user_id=demo["user_id"],
            booking_date=demo["booking_date"],
            amount=demo["amount"],
            currency=demo["currency"],
            direction=demo["direction"],
            counterparty=demo["counterparty"],
            concept=demo["concept"],
            status=demo["status"],
        )
        session.add(event)

    session.commit()
