import re
import unicodedata

from app.schemas.chat import ChatIntent, EntityValue, IntentDecision
from app.services.chat_taxonomy import INTENT_TOOL_MAP


KNOWN_ACCOUNT_ALIASES = {
    "nomina": "Nómina",
    "ahorro": "Ahorro",
    "gastos": "Gastos",
    "principal": "Principal",
}


def _normalize_text(message: str) -> str:
    text = message.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[¿?¡!.,;:]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def build_intent_prompt(message: str) -> str:
    return f"""
You are an intent and entity detection agent for a banking assistant.

Your task:
1. Detect the main banking intent.
2. Extract entities if present.
3. Detect missing entities required to complete the operation.
4. If required information is missing, produce a clarification question.

Allowed intents:
- BALANCE_SUMMARY
- ACCOUNTS
- RECENT_TRANSACTIONS
- RECENT_BIZUM
- RECEIVED_BIZUM
- FALLBACK

Possible entities:
- account_alias
- account_id
- limit
- date_range
- category
- counterparty
- direction

Rules:
- BALANCE_SUMMARY may optionally refer to a specific account.
- ACCOUNTS usually needs no extra entities.
- RECENT_TRANSACTIONS may include account, date range, category or limit.
- RECENT_BIZUM may include limit, direction or counterparty.
- RECEIVED_BIZUM may include limit or counterparty.
- FALLBACK if the request is outside supported banking capabilities.

Return a structured result with:
- intent
- confidence
- reason
- tool_name
- entities
- missing_entities
- needs_clarification
- clarification_question

User message:
{message}
""".strip()


def _extract_account_alias(text: str) -> EntityValue | None:
    for normalized_alias, original_alias in KNOWN_ACCOUNT_ALIASES.items():
        if normalized_alias in text:
            return EntityValue(
                name="account_alias",
                value=original_alias,
                normalized_value=normalized_alias,
                confidence=0.90,
            )
    return None


def _extract_limit(text: str) -> EntityValue | None:
    match = re.search(r"\b(\d{1,2})\b", text)
    if not match:
        return None

    return EntityValue(
        name="limit",
        value=match.group(1),
        normalized_value=match.group(1),
        confidence=0.80,
    )


def _extract_entities(intent: ChatIntent, text: str) -> list[EntityValue]:
    entities: list[EntityValue] = []

    account_alias = _extract_account_alias(text)
    if account_alias:
        entities.append(account_alias)

    limit = _extract_limit(text)
    if limit and intent in {
        ChatIntent.RECENT_TRANSACTIONS,
        ChatIntent.RECENT_BIZUM,
        ChatIntent.RECEIVED_BIZUM,
    }:
        entities.append(limit)

    return entities


def _needs_clarification(
    intent: ChatIntent,
    text: str,
    entities: list[EntityValue],
) -> tuple[list[str], bool, str | None]:
    entity_names = {entity.name for entity in entities}

    if intent == ChatIntent.BALANCE_SUMMARY and "cuenta" in text:
        if "account_alias" not in entity_names:
            return (
                ["account_alias"],
                True,
                "¿Sobre qué cuenta quieres consultar el saldo?",
            )

    if intent == ChatIntent.RECENT_TRANSACTIONS and "cuenta" in text:
        if "account_alias" not in entity_names:
            return (
                ["account_alias"],
                True,
                "¿De qué cuenta quieres ver los movimientos?",
            )

    return ([], False, None)


def classify_intent(message: str) -> IntentDecision:
    text = _normalize_text(message)

    if "saldo" in text or "balance" in text or "dinero tengo" in text:
        intent = ChatIntent.BALANCE_SUMMARY
        confidence = 0.90
        reason = "Message mentions balance or available money."
    elif (
        "mis cuentas" in text
        or "que cuentas tengo" in text
        or text.startswith("cuentas")
    ):
        intent = ChatIntent.ACCOUNTS
        confidence = 0.92
        reason = "Message asks about bank accounts."
    elif (
        "ultimos movimientos" in text
        or "movimientos recientes" in text
        or "gastos recientes" in text
    ):
        intent = ChatIntent.RECENT_TRANSACTIONS
        confidence = 0.90
        reason = "Message asks about recent transactions."
    elif "bizum recibidos" in text or "he recibido algun bizum" in text:
        intent = ChatIntent.RECEIVED_BIZUM
        confidence = 0.93
        reason = "Message explicitly asks about received Bizum."
    elif "bizum" in text:
        intent = ChatIntent.RECENT_BIZUM
        confidence = 0.85
        reason = "Message mentions Bizum in a generic way."
    else:
        intent = ChatIntent.FALLBACK
        confidence = 0.40
        reason = "No supported banking intent detected."

    entities = _extract_entities(intent, text)
    missing_entities, needs_clarification, clarification_question = (
        _needs_clarification(
            intent=intent,
            text=text,
            entities=entities,
        )
    )

    return IntentDecision(
        intent=intent,
        confidence=confidence,
        reason=reason,
        tool_name=INTENT_TOOL_MAP[intent],
        entities=entities,
        missing_entities=missing_entities,
        needs_clarification=needs_clarification,
        clarification_question=clarification_question,
    )
