from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.data.accounts import (
    get_detailed_balance_summary_by_user_id,
    get_public_accounts_by_user_id,
)
from app.schemas.accounts import AccountPublic, BalanceSummaryDetailed
from app.schemas.user import UserPublic


router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("", response_model=list[AccountPublic])
def list_accounts(current_user: UserPublic = Depends(get_current_user)):
    return get_public_accounts_by_user_id(current_user.user_id)

@router.get("/summary", response_model=BalanceSummaryDetailed)
def get_accounts_summary(current_user: UserPublic = Depends(get_current_user)):
    return get_detailed_balance_summary_by_user_id(current_user.user_id)