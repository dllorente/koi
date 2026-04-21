from app.schemas.chat import ChatIntent

INTENT_REQUIRED_ENTITIES: dict[ChatIntent, list[str]] = {
    ChatIntent.BALANCE_SUMMARY: [],
    ChatIntent.ACCOUNTS: [],
    ChatIntent.RECENT_TRANSACTIONS: [],
    ChatIntent.RECENT_BIZUM: [],
    ChatIntent.RECEIVED_BIZUM: [],
    ChatIntent.FALLBACK: [],
}
INTENT_OPTIONAL_ENTITIES: dict[ChatIntent, list[str]] = {
    ChatIntent.BALANCE_SUMMARY: ["account_alias"],
    ChatIntent.ACCOUNTS: [],
    ChatIntent.RECENT_TRANSACTIONS: ["account_alias"],
    ChatIntent.RECENT_BIZUM: [],
    ChatIntent.RECEIVED_BIZUM: [],
    ChatIntent.FALLBACK: [],
}
INTENT_TOOL_MAP: dict[ChatIntent, str | None] = {
    ChatIntent.BALANCE_SUMMARY: "get_balance_summary",
    ChatIntent.ACCOUNTS: "get_accounts",
    ChatIntent.RECENT_TRANSACTIONS: "get_recent_transactions",
    ChatIntent.RECENT_BIZUM: "get_recent_bizum",
    ChatIntent.RECEIVED_BIZUM: "get_received_bizum",
    ChatIntent.FALLBACK: None,
}
