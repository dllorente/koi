from pydantic import BaseModel
from enum import Enum
from typing import Any

class ChatIntent(str, Enum):
    BALANCE_SUMMARY = "BALANCE_SUMMARY"
    ACCOUNTS = "ACCOUNTS"
    RECENT_TRANSACTIONS = "RECENT_TRANSACTIONS"
    RECENT_BIZUM = "RECENT_BIZUM"
    RECEIVED_BIZUM = "RECEIVED_BIZUM"
    FALLBACK = "FALLBACK"
    
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



