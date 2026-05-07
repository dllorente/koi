from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.models import ChatSession, ChatMessage
from app.api.deps import get_current_user
from app.db.database import get_session
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatSessionResponse,
    ChatHistoryResponse,
)
from app.schemas.user import UserPublic
from app.services.chat_router import handle_chat
from fastapi import HTTPException

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: UserPublic = Depends(get_current_user),
) -> ChatResponse:
    return handle_chat(
        session=session,
        message=request.message,
        user_id=current_user.user_id,
        session_id=request.session_id,
    )


@router.get("/sessions", response_model=list[ChatSessionResponse])
def list_chat_sessions(
    session: Session = Depends(get_session),
    current_user: UserPublic = Depends(get_current_user),
):
    stmt = (
        select(ChatSession)
        .where(ChatSession.user_id == current_user.user_id)
        .order_by(ChatSession.updated_at.desc())
    )
    sessions = session.exec(stmt).all()

    return [
        {
            "session_id": s.session_id,
            "user_id": s.user_id,
            "title": s.title,
            "created_at": s.created_at,
            "updated_at": s.updated_at,
        }
        for s in sessions
    ]


@router.get("/sessions/{session_id}/messages", response_model=ChatHistoryResponse)
def get_session_messages(
    session_id: str,
    session: Session = Depends(get_session),
    current_user: UserPublic = Depends(get_current_user),
):
    chat_session = session.exec(
        select(ChatSession)
        .where(ChatSession.session_id == session_id)
        .where(ChatSession.user_id == current_user.user_id)
    ).first()

    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    messages = session.exec(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    ).all()

    return {
        "session_id": session_id,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "intent": m.intent,
                "tool_name": m.tool_name,
                "needs_clarification": m.needs_clarification,
                "clarification_question": m.clarification_question,
                "entities_json": m.entities_json,
                "missing_entities_json": m.missing_entities_json,
                "decision_reason": m.decision_reason,
                "decision_confidence": m.decision_confidence,
                "created_at": m.created_at,
            }
            for m in messages
        ],
    }
