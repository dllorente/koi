from sqlmodel import Session,select
from app.schemas.transaction import TransactionListResponse, TransactionPublic
from app.db.models import Transaction

def get_transactions_by_user_id(session: Session, user_id: str) -> list[Transaction]:
    statement = (
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.booking_date.desc())
    )
    return session.exec(statement).all()

def get_transactions_by_account_id(session: Session, account_id: str) -> list[Transaction]:
    statement = (
        select(Transaction)
        .where(Transaction.account_id == account_id)
        .order_by(Transaction.booking_date.desc())
    )
    return session.exec(statement).all()


def get_public_transactions_by_user_id(
    session: Session,
    user_id: str,
    limit: int = 10,
) -> TransactionListResponse:
    transactions = get_transactions_by_user_id(session, user_id)[:limit]

    items = [
        TransactionPublic(
            transaction_id=tx.transaction_id,
            account_id=tx.account_id,
            booking_date=tx.booking_date,
            amount=tx.amount,
            currency=tx.currency,
            description=tx.description,
            category=tx.category,
        )
        for tx in transactions
    ]

    return TransactionListResponse(items=items, count=len(items))


def get_public_transactions_by_account_id(
    session: Session,
    account_id: str,
    limit: int = 10,
) -> TransactionListResponse:
    transactions = get_transactions_by_account_id(session, account_id)[:limit]

    items = [
        TransactionPublic(
            transaction_id=tx.transaction_id,
            account_id=tx.account_id,
            booking_date=tx.booking_date,
            amount=tx.amount,
            currency=tx.currency,
            description=tx.description,
            category=tx.category,
        )
        for tx in transactions
    ]

    return TransactionListResponse(items=items, count=len(items))