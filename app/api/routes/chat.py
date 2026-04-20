from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.deps import get_current_user
from app.db.database import get_session
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.user import UserPublic
from app.services.chat_router import handle_chat

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: UserPublic = Depends(get_current_user),
)-> ChatResponse:
    return handle_chat(
        session=session,
        message=request.message,
        user_id=current_user.user_id,
        session_id=request.session_id,
    )