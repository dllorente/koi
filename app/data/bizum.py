# app/data/bizum.py
from sqlmodel import Session, select

from app.db.models import BizumEvent
from app.schemas.bizum import BizumEventPublic, BizumListResponse


def get_public_bizum_events_by_user_id(
    session: Session,
    user_id: str,
    limit: int = 10,
) -> BizumListResponse:
    statement = (
        select(BizumEvent)
        .where(BizumEvent.user_id == user_id)
        .order_by(BizumEvent.booking_date.desc())
        .limit(limit)
    )
    events = session.exec(statement).all()

    items = [
        BizumEventPublic(
            bizum_id=event.bizum_id,
            booking_date=event.booking_date,
            amount=event.amount,
            currency=event.currency,
            direction=event.direction,
            counterparty=event.counterparty,
            concept=event.concept,
            status=event.status,
        )
        for event in events
    ]

    return BizumListResponse(
        items=items,
        count=len(items),
    )


def get_received_bizum_events_by_user_id(
    session: Session,
    user_id: str,
    limit: int = 10,
) -> BizumListResponse:
    statement = (
        select(BizumEvent)
        .where(BizumEvent.user_id == user_id)
        .where(BizumEvent.direction == "received")
        .order_by(BizumEvent.booking_date.desc())
        .limit(limit)
    )
    events = session.exec(statement).all()

    items = [
        BizumEventPublic(
            bizum_id=event.bizum_id,
            booking_date=event.booking_date,
            amount=event.amount,
            currency=event.currency,
            direction=event.direction,
            counterparty=event.counterparty,
            concept=event.concept,
            status=event.status,
        )
        for event in events
    ]

    return BizumListResponse(
        items=items,
        count=len(items),
    )
