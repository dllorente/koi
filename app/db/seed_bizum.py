from sqlmodel import Session, select
from datetime import date

from app.db.models import BizumEvent


def seed_bizum(session: Session) -> None:
    existing = session.exec(select(BizumEvent)).first()
    if existing:
        return

    items = [
        BizumEvent(
            bizum_id="bizum-001",
            user_id="u001",
            booking_date=date(2026, 4, 18),
            amount=25.0,
            currency="EUR",
            direction="received",
            counterparty="Ana",
            concept="Cena",
            status="completed",
        ),
        BizumEvent(
            bizum_id="bizum-002",
            user_id="u001",
            booking_date=date(2026, 4, 17),
            amount=12.5,
            currency="EUR",
            direction="sent",
            counterparty="Carlos",
            concept="Taxi",
            status="completed",
        ),
        BizumEvent(
            bizum_id="bizum-003",
            user_id="u001",
            booking_date=date(2026, 4, 16),
            amount=40.0,
            currency="EUR",
            direction="received",
            counterparty="Lucía",
            concept="Regalo compartido",
            status="completed",
        ),
    ]

    for item in items:
        session.add(item)

    session.commit()