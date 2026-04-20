from sqlmodel import Session
import re
import unicodedata
from app.db.models import ChatMessage
from app.schemas.chat import ChatResponse, ChatIntent, ChatSuggestion
from app.data.transactions import get_public_transactions_by_user_id
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

def _save_chat_message(
    session: Session,
    session_id: str,
    user_id: str,
    role: str,
    content: str,
) -> None:
    message = ChatMessage(
        session_id=session_id,
        user_id=user_id,
        role=role,
        content=content,
    )
    session.add(message)
    session.commit()


def handle_chat(
    session: Session,
    message: str,
    user_id: str,
    session_id: str,
) -> ChatResponse:
    _save_chat_message(
        session=session,
        session_id=session_id,
        user_id=user_id,
        role="user",
        content=message,
    )

    intent = detect_intent(message)

    if intent == ChatIntent.BALANCE_SUMMARY:
        summary = get_detailed_balance_summary_by_user_id(session, user_id)

        response = ChatResponse(
            answer=(
                f"Tienes un saldo total de {summary.total_balance} {summary.currency} "
                f"repartido en {summary.account_count} cuentas."
            ),
            intent=intent.value,
            data={
                "total_balance": summary.total_balance,
                "currency": summary.currency,
                "account_count": summary.account_count,
            },
            suggestions=[
                ChatSuggestion(
                    id="accounts_list",
                    label="Ver cuentas",
                    prompt="Muéstrame mis cuentas",
                    kind="chip",
                    category="accounts",
                ),
                ChatSuggestion(
                    id="recent_transactions",
                    label="Últimos movimientos",
                    prompt="Muéstrame mis últimos movimientos",
                    kind="chip",
                    category="transactions",
                ),
            ],
            ui_hints={
                "component": "balance_summary_card",
            },
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
        )
        return response

    if intent == ChatIntent.ACCOUNTS:
        accounts = get_public_accounts_by_user_id(session, user_id)

        if not accounts:
            response = ChatResponse(
                answer="No he encontrado cuentas asociadas a tu usuario.",
                intent=intent.value,
                data={
                    "accounts": [],
                    "count": 0,
                },
                suggestions=[
                    ChatSuggestion(
                        id="balance_summary",
                        label="Ver saldo total",
                        prompt="¿Cuál es mi saldo total?",
                        kind="chip",
                        category="accounts",
                    )
                ],
                ui_hints={
                    "component": "account_list",
                },
            )

            _save_chat_message(
                session=session,
                session_id=session_id,
                user_id=user_id,
                role="assistant",
                content=response.answer,
            )
            return response

        account_lines = [f"- {acc.alias}: {acc.balance} {acc.currency}" for acc in accounts]

        response = ChatResponse(
            answer="Estas son tus cuentas:\n" + "\n".join(account_lines),
            intent=intent.value,
            data={
                "accounts": [
                    {
                        "account_id": acc.account_id,
                        "alias": acc.alias,
                        "balance": acc.balance,
                        "currency": acc.currency,
                    }
                    for acc in accounts
                ],
                "count": len(accounts),
            },
            suggestions=[
                ChatSuggestion(
                    id="balance_summary",
                    label="Saldo total",
                    prompt="¿Cuál es mi saldo total?",
                    kind="chip",
                    category="accounts",
                ),
                ChatSuggestion(
                    id="recent_transactions",
                    label="Últimos movimientos",
                    prompt="Muéstrame mis últimos movimientos",
                    kind="chip",
                    category="transactions",
                ),
            ],
            ui_hints={
                "component": "account_list",
            },
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
        )
        return response

    if intent == ChatIntent.RECENT_TRANSACTIONS:
        tx_response = get_public_transactions_by_user_id(session, user_id, limit=5)

        if not tx_response.items:
            response = ChatResponse(
                answer="No he encontrado movimientos recientes.",
                intent=intent.value,
                data={
                    "items": [],
                    "count": 0,
                },
                suggestions=[
                    ChatSuggestion(
                        id="accounts_list",
                        label="Ver cuentas",
                        prompt="Muéstrame mis cuentas",
                        kind="chip",
                        category="accounts",
                    )
                ],
                ui_hints={
                    "component": "transaction_list",
                },
            )

            _save_chat_message(
                session=session,
                session_id=session_id,
                user_id=user_id,
                role="assistant",
                content=response.answer,
            )
            return response

        lines = [
            f"- {tx.booking_date}: {tx.description} ({tx.amount} {tx.currency})"
            for tx in tx_response.items
        ]

        response = ChatResponse(
            answer="Estos son tus últimos movimientos:\n" + "\n".join(lines),
            intent=intent.value,
            data={
                "items": [
                    {
                        "transaction_id": tx.transaction_id,
                        "account_id": tx.account_id,
                        "booking_date": str(tx.booking_date),
                        "amount": tx.amount,
                        "currency": tx.currency,
                        "description": tx.description,
                        "category": tx.category,
                    }
                    for tx in tx_response.items
                ],
                "count": tx_response.count,
            },
            suggestions=[
                ChatSuggestion(
                    id="accounts_list",
                    label="Ver cuentas",
                    prompt="Muéstrame mis cuentas",
                    kind="chip",
                    category="accounts",
                ),
                ChatSuggestion(
                    id="recent_bizum",
                    label="Bizum reciente",
                    prompt="Enséñame mi actividad reciente de Bizum",
                    kind="chip",
                    category="bizum",
                ),
            ],
            ui_hints={
                "component": "transaction_list",
            },
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
        )
        return response

    if intent == ChatIntent.RECENT_BIZUM:
        bizum_response = get_public_bizum_events_by_user_id(session, user_id, limit=5)

        if not bizum_response.items:
            response = ChatResponse(
                answer="No he encontrado actividad reciente de Bizum.",
                intent=intent.value,
                data={
                    "items": [],
                    "count": 0,
                },
                suggestions=[
                    ChatSuggestion(
                        id="recent_transactions",
                        label="Ver movimientos",
                        prompt="Muéstrame mis últimos movimientos",
                        kind="chip",
                        category="transactions",
                    )
                ],
                ui_hints={
                    "component": "bizum_list",
                },
            )

            _save_chat_message(
                session=session,
                session_id=session_id,
                user_id=user_id,
                role="assistant",
                content=response.answer,
            )
            return response

        lines = [
            f"- {event.booking_date}: {event.direction} {event.amount} {event.currency} con {event.counterparty}"
            for event in bizum_response.items
        ]

        response = ChatResponse(
            answer="Esta es tu actividad reciente de Bizum:\n" + "\n".join(lines),
            intent=intent.value,
            data={
                "items": [
                    {
                        "bizum_id": event.bizum_id,
                        "booking_date": str(event.booking_date),
                        "amount": event.amount,
                        "currency": event.currency,
                        "direction": event.direction,
                        "counterparty": event.counterparty,
                        "concept": event.concept,
                        "status": event.status,
                    }
                    for event in bizum_response.items
                ],
                "count": bizum_response.count,
            },
            suggestions=[
                ChatSuggestion(
                    id="received_bizum",
                    label="Bizum recibidos",
                    prompt="Muéstrame mis Bizum recibidos",
                    kind="chip",
                    category="bizum",
                ),
                ChatSuggestion(
                    id="recent_transactions",
                    label="Últimos movimientos",
                    prompt="Muéstrame mis últimos movimientos",
                    kind="chip",
                    category="transactions",
                ),
            ],
            ui_hints={
                "component": "bizum_list",
            },
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
        )
        return response

    if intent == ChatIntent.RECEIVED_BIZUM:
        bizum_response = get_received_bizum_events_by_user_id(session, user_id, limit=5)

        if not bizum_response.items:
            response = ChatResponse(
                answer="No he encontrado Bizum recibidos recientemente.",
                intent=intent.value,
                data={
                    "items": [],
                    "count": 0,
                },
                suggestions=[
                    ChatSuggestion(
                        id="recent_bizum",
                        label="Bizum reciente",
                        prompt="Enséñame mi actividad reciente de Bizum",
                        kind="chip",
                        category="bizum",
                    )
                ],
                ui_hints={
                    "component": "bizum_list",
                },
            )

            _save_chat_message(
                session=session,
                session_id=session_id,
                user_id=user_id,
                role="assistant",
                content=response.answer,
            )
            return response

        lines = [
            f"- {event.booking_date}: {event.amount} {event.currency} de {event.counterparty}"
            for event in bizum_response.items
        ]

        response = ChatResponse(
            answer="Estos son tus últimos Bizum recibidos:\n" + "\n".join(lines),
            intent=intent.value,
            data={
                "items": [
                    {
                        "bizum_id": event.bizum_id,
                        "booking_date": str(event.booking_date),
                        "amount": event.amount,
                        "currency": event.currency,
                        "direction": event.direction,
                        "counterparty": event.counterparty,
                        "concept": event.concept,
                        "status": event.status,
                    }
                    for event in bizum_response.items
                ],
                "count": bizum_response.count,
            },
            suggestions=[
                ChatSuggestion(
                    id="recent_bizum",
                    label="Bizum reciente",
                    prompt="Enséñame mi actividad reciente de Bizum",
                    kind="chip",
                    category="bizum",
                ),
                ChatSuggestion(
                    id="accounts_list",
                    label="Ver cuentas",
                    prompt="Muéstrame mis cuentas",
                    kind="chip",
                    category="accounts",
                ),
            ],
            ui_hints={
                "component": "bizum_list",
            },
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
        )
        return response

    response = ChatResponse(
        answer="Todavía no puedo responder a esa consulta. Por ahora prueba con saldo, cuentas, movimientos o Bizum.",
        intent=intent.value,
        data=None,
        suggestions=[
            ChatSuggestion(
                id="balance_summary",
                label="Saldo total",
                prompt="¿Cuál es mi saldo total?",
                kind="chip",
                category="accounts",
            ),
            ChatSuggestion(
                id="accounts_list",
                label="Mis cuentas",
                prompt="Muéstrame mis cuentas",
                kind="chip",
                category="accounts",
            ),
            ChatSuggestion(
                id="recent_transactions",
                label="Últimos movimientos",
                prompt="Muéstrame mis últimos movimientos",
                kind="chip",
                category="transactions",
            ),
            ChatSuggestion(
                id="recent_bizum",
                label="Bizum reciente",
                prompt="Enséñame mi actividad reciente de Bizum",
                kind="chip",
                category="bizum",
            ),
        ],
        ui_hints={
            "component": "fallback_message",
        },
    )

    _save_chat_message(
        session=session,
        session_id=session_id,
        user_id=user_id,
        role="assistant",
        content=response.answer,
    )
    return response