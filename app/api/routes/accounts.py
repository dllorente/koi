from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.api.deps import get_current_user
from app.schemas.accounts import AccountPublic, BalanceSummaryDetailed
from app.data.accounts import (
    get_public_accounts_by_user_id,
    get_detailed_balance_summary_by_user_id,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountPublic])
def list_accounts(
    session: Session = Depends(get_session), current_user=Depends(get_current_user)
):
    return get_public_accounts_by_user_id(session, current_user.user_id)


@router.get("/summary", response_model=BalanceSummaryDetailed)
def get_accounts_summary(
    session: Session = Depends(get_session), current_user=Depends(get_current_user)
):
    return get_detailed_balance_summary_by_user_id(session, current_user.user_id)
