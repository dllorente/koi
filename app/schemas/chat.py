from pydantic import BaseModel, Field
from enum import Enum
from typing import Any
from datetime import datetime


class EntityValue(BaseModel):
    name: str
    value: str
    normalized_value: str | None = None
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)


class ChatIntent(str, Enum):
    BALANCE_SUMMARY = "BALANCE_SUMMARY"
    ACCOUNTS = "ACCOUNTS"
    RECENT_TRANSACTIONS = "RECENT_TRANSACTIONS"
    RECENT_BIZUM = "RECENT_BIZUM"
    RECEIVED_BIZUM = "RECEIVED_BIZUM"
    FALLBACK = "FALLBACK"


class IntentDecision(BaseModel):
    intent: ChatIntent
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str | None = None
    tool_name: str | None = None
    entities: list[EntityValue] = Field(default_factory=list)
    missing_entities: list[str] = Field(default_factory=list)
    needs_clarification: bool = False
    clarification_question: str | None = None
    source: str | None = None


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatSuggestion(BaseModel):
    id: str | None = None
    label: str
    prompt: str
    kind: str = "chip"
    category: str | None = None


class ChatResponse(BaseModel):
    answer: str
    intent: ChatIntent
    session_id: str
    data: dict[str, Any] | None = None
    suggestions: list[ChatSuggestion] = Field(default_factory=list)
    ui_hints: dict[str, Any] | None = None
    tools_used: list[str] = Field(default_factory=list)
    needs_clarification: bool = False
    clarification_question: str | None = None
    decision_confidence: float | None = None
    decision_reason: str | None = None


class ChatMessageResponse(BaseModel):
    id: int
    user_id: str | None = None
    role: str
    content: str
    intent: str | None = None
    tool_name: str | None = None
    needs_clarification: bool = False
    clarification_question: str | None = None
    entities_json: str | None = None
    missing_entities_json: str | None = None
    decision_reason: str | None = None
    decision_confidence: float | None = None
    created_at: datetime


class ChatSessionResponse(BaseModel):
    session_id: str
    user_id: str
    title: str | None = None
    created_at: datetime
    updated_at: datetime


class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: list[ChatMessageResponse] = Field(default_factory=list)
