from datetime import date, timedelta
from sqlmodel import Session, select

from app.db.models import Account, Transaction, User


def seed_transactions(session: Session) -> None:
    # ¿ya hay transacciones?
    existing = session.exec(select(Transaction)).first()
    if existing:
        return

    today = date.today()

    # Por cada cuenta, generamos algunos movimientos de ejemplo
    accounts = session.exec(select(Account)).all()

    tx_counter = 1
    for account in accounts:
        # buscamos el usuario asociado a la cuenta
        user = session.exec(select(User).where(User.user_id == account.user_id)).first()
        if not user:
            continue

        # generamos 5 movimientos por cuenta
        for i in range(5):
            tx = Transaction(
                transaction_id=f"tx-{tx_counter:06d}",
                user_id=account.user_id,
                account_id=account.account_id,
                booking_date=today - timedelta(days=i),
                amount=round(50 * (i + 1) * (-1 if i % 2 == 0 else 1), 2),
                currency=account.currency,
                description=f"Movimiento demo {i + 1} en {account.alias}",
                category="demo",
            )
            session.add(tx)
            tx_counter += 1

    session.commit()
