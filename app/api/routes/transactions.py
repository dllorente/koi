from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_user
from app.data.accounts import get_accounts_by_user_id
from app.data.transactions import (
    get_public_transactions_by_account_id,
    get_public_transactions_by_user_id,
)
from app.schemas.transaction import TransactionListResponse
from app.schemas.user import UserPublic
from sqlmodel import Session
from app.db.database import get_session


router = APIRouter(prefix="/transactions", tags=["transactions"])

#Devuelve los últimos movimientos del usuario autenticado.
@router.get("/recent", response_model=TransactionListResponse)
def get_recent_transactions(
    limit: int = Query(default=10, ge=1, le=50),
    current_user: UserPublic = Depends(get_current_user),
    session: Session = Depends(get_session)

):
    return get_public_transactions_by_user_id(session,current_user.user_id, limit=limit)

#Devuelve movimientos de una cuenta concreta, pero solo si esa cuenta pertenece al usuario autenticado.
@router.get("/accounts/{account_id}", response_model=TransactionListResponse)
def get_account_transactions(
    account_id: str,
    limit: int = Query(default=10, ge=1, le=50),
    session: Session = Depends(get_session),
    current_user: UserPublic = Depends(get_current_user),
    
):
    user_accounts = get_accounts_by_user_id(session,current_user.user_id)
    account_ids = {acc.account_id for acc in user_accounts}

    if account_id not in account_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found for current user",
        )

    return get_public_transactions_by_account_id(session,account_id, limit=limit)