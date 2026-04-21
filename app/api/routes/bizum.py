from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_current_user
from app.data.bizum import (
    get_public_bizum_events_by_user_id,
    get_received_bizum_events_by_user_id,
)
from app.db.database import get_session
from app.schemas.bizum import BizumListResponse
from app.schemas.user import UserPublic

router = APIRouter(prefix="/bizum", tags=["bizum"])


# Devuelve la actividad Bizum reciente del usuario autenticado.
@router.get("/recent", response_model=BizumListResponse)
def get_recent_bizum_events(
    limit: int = Query(default=10, ge=1, le=50),
    session: Session = Depends(get_session),
    current_user: UserPublic = Depends(get_current_user),
):
    return get_public_bizum_events_by_user_id(
        session,
        current_user.user_id,
        limit=limit,
    )


# Devuelve solo los Bizum recibidos del usuario autenticado.
@router.get("/received", response_model=BizumListResponse)
def get_received_bizum_events(
    limit: int = Query(default=10, ge=1, le=50),
    session: Session = Depends(get_session),
    current_user: UserPublic = Depends(get_current_user),
):
    return get_received_bizum_events_by_user_id(
        session,
        current_user.user_id,
        limit=limit,
    )
