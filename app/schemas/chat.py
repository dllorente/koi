from pydantic import BaseModel
from enum import Enum

class ChatIntent(str, Enum):
    BALANCE_SUMMARY = "balance_summary"
    ACCOUNTS = "accounts"
    RECENT_TRANSACTIONS = "recent_transactions"
    RECENT_BIZUM = "recent_bizum"
    RECEIVED_BIZUM = "received_bizum"
    FALLBACK = "fallback"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    intent: ChatIntent