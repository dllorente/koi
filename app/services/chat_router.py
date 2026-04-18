import re
import unicodedata

from app.data.transactions import get_public_transactions_by_user_id
from app.schemas.chat import ChatIntent
from app.data.accounts import (
    get_detailed_balance_summary_by_user_id,
    get_public_accounts_by_user_id,
)
from app.data.bizum import (
    get_public_bizum_events_by_user_id,
    get_received_bizum_events_by_user_id,
)

def _normalize_text(message: str) -> str:
    text = message.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[¿?¡!.,;:]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def detect_intent(message: str) -> ChatIntent:
    text = _normalize_text(message)

    if "saldo" in text or "balance" in text or "dinero tengo" in text:
        return ChatIntent.BALANCE_SUMMARY

    if "mis cuentas" in text or "que cuentas tengo" in text or text.startswith("cuentas"):
        return ChatIntent.ACCOUNTS

    if "ultimos movimientos" in text or "movimientos recientes" in text or "gastos recientes" in text:
        return ChatIntent.RECENT_TRANSACTIONS

    if "bizum recibidos" in text or "he recibido algun bizum" in text:
        return ChatIntent.RECEIVED_BIZUM

    if "bizum" in text:
        return ChatIntent.RECENT_BIZUM

    return ChatIntent.FALLBACK



def handle_chat(message: str, user_id: str) -> tuple[str, ChatIntent]:
    intent = detect_intent(message)

    if intent == ChatIntent.BALANCE_SUMMARY:
        summary = get_detailed_balance_summary_by_user_id(user_id)
        answer = (
            f"Tienes un saldo total de {summary.total_balance} {summary.currency} "
            f"repartido en {summary.account_count} cuentas."
        )
        return answer, intent

    if intent == ChatIntent.ACCOUNTS:
        accounts = get_public_accounts_by_user_id(user_id)
        if not accounts:
            return "No he encontrado cuentas asociadas a tu usuario.", intent

        account_lines = [f"- {acc.alias}: {acc.balance} {acc.currency}" for acc in accounts]
        answer = "Estas son tus cuentas:\n" + "\n".join(account_lines)
        return answer, intent

    if intent == ChatIntent.RECENT_TRANSACTIONS:
        tx_response = get_public_transactions_by_user_id(user_id, limit=5)
        if not tx_response.items:
            return "No he encontrado movimientos recientes.", intent

        lines = [
            f"- {tx.booking_date}: {tx.description} ({tx.amount} {tx.currency})"
            for tx in tx_response.items
        ]
        answer = "Estos son tus últimos movimientos:\n" + "\n".join(lines)
        return answer, intent

    if intent == ChatIntent.RECENT_BIZUM:
        bizum_response = get_public_bizum_events_by_user_id(user_id, limit=5)
        if not bizum_response.items:
            return "No he encontrado actividad reciente de Bizum.", intent

        lines = [
            f"- {event.booking_date}: {event.direction} {event.amount} {event.currency} con {event.counterparty}"
            for event in bizum_response.items
        ]
        answer = "Esta es tu actividad reciente de Bizum:\n" + "\n".join(lines)
        return answer, intent

    if intent == ChatIntent.RECEIVED_BIZUM:
        bizum_response = get_received_bizum_events_by_user_id(user_id, limit=5)
        if not bizum_response.items:
            return "No he encontrado Bizum recibidos recientemente.", intent

        lines = [
            f"- {event.booking_date}: {event.amount} {event.currency} de {event.counterparty}"
            for event in bizum_response.items
        ]
        answer = "Estos son tus últimos Bizum recibidos:\n" + "\n".join(lines)
        return answer, intent

    return (
        "Todavía no puedo responder a esa consulta. Por ahora prueba con saldo, cuentas, movimientos o Bizum.",
        intent,
    )