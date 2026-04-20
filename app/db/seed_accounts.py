from sqlmodel import Session, select

from app.db.models import User, Account
from app.data.accounts import DEMO_ACCOUNTS  


def seed_accounts(session: Session) -> None:
    for demo in DEMO_ACCOUNTS:
        existing_account = session.exec(
            select(Account).where(Account.account_id == demo["account_id"])
        ).first()

        if existing_account:
            continue

        user_exists = session.exec(
            select(User).where(User.user_id == demo["user_id"])
        ).first()

        if not user_exists:
            continue

        account = Account(
            account_id=demo["account_id"],
            user_id=demo["user_id"],
            iban=demo["iban"],
            alias=demo["alias"],
            balance=demo["balance"],
            currency=demo["currency"],
        )
        session.add(account)

    session.commit()