from pydantic import BaseModel, Field
from enum import Enum
from typing import Any


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
    entities: list[EntityValue] = []
    missing_entities: list[str] = []
    needs_clarification: bool = False
    clarification_question: str | None = None


class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatSuggestion(BaseModel):
    id: str | None = None
    label: str
    prompt: str
    kind: str = "chip"
    category: str | None = None


class ChatResponse(BaseModel):
    answer: str
    intent: ChatIntent
    data: dict[str, Any] | None = None
    suggestions: list[ChatSuggestion] = []
    ui_hints: dict[str, Any] | None = None
    tools_used: list[str] = []
