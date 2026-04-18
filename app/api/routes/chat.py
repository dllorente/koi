from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.user import UserPublic
from app.services.chat_router import handle_chat

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)

def chat(
    request: ChatRequest,
    current_user: UserPublic = Depends(get_current_user),
):
    answer, intent = handle_chat(request.message, current_user.user_id)
    return ChatResponse(answer=answer, intent=intent)
