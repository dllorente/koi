import json
import re
import unicodedata

from sqlmodel import Session, select

from app.data.accounts import (
    get_detailed_balance_summary_by_user_id,
    get_public_accounts_by_user_id,
)
from app.data.bizum import (
    get_public_bizum_events_by_user_id,
    get_received_bizum_events_by_user_id,
)
from app.data.transactions import get_public_transactions_by_user_id
from app.db.models import ChatMessage
from app.schemas.chat import (
    ChatIntent,
    ChatResponse,
    ChatSuggestion,
    IntentDecision,
)
from app.services.chat_taxonomy import (
    INTENT_OPTIONAL_ENTITIES,
    INTENT_REQUIRED_ENTITIES,
    INTENT_TOOL_MAP,
)
from app.services.intent_agent import classify_intent


def _get_tool_name_for_intent(intent: ChatIntent) -> str | None:
    return INTENT_TOOL_MAP.get(intent)


def _get_required_entities(intent: ChatIntent) -> list[str]:
    return INTENT_REQUIRED_ENTITIES.get(intent, [])


def _get_optional_entities(intent: ChatIntent) -> list[str]:
    return INTENT_OPTIONAL_ENTITIES.get(intent, [])


def _normalize_text(message: str) -> str:
    text = message.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[¿?¡!.,;:]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def detect_intent_rule_based(message: str) -> IntentDecision:
    text = _normalize_text(message)

    if "saldo" in text or "balance" in text or "dinero tengo" in text:
        return IntentDecision(
            intent=ChatIntent.BALANCE_SUMMARY,
            confidence=0.95,
            reason="Detected clear balance-related keywords",
            tool_name=_get_tool_name_for_intent(ChatIntent.BALANCE_SUMMARY),
        )

    if (
        "mis cuentas" in text
        or "que cuentas tengo" in text
        or text.startswith("cuentas")
    ):
        return IntentDecision(
            intent=ChatIntent.ACCOUNTS,
            confidence=0.95,
            reason="Detected clear accounts-related keywords",
            tool_name=_get_tool_name_for_intent(ChatIntent.ACCOUNTS),
        )

    if (
        "ultimos movimientos" in text
        or "movimientos recientes" in text
        or "gastos recientes" in text
        or "movimientos" in text
    ):
        return IntentDecision(
            intent=ChatIntent.RECENT_TRANSACTIONS,
            confidence=0.90,
            reason="Detected transactions-related keywords",
            tool_name=_get_tool_name_for_intent(ChatIntent.RECENT_TRANSACTIONS),
        )

    if "bizum recibidos" in text or "he recibido algun bizum" in text:
        return IntentDecision(
            intent=ChatIntent.RECEIVED_BIZUM,
            confidence=0.95,
            reason="Detected received Bizum request",
            tool_name=_get_tool_name_for_intent(ChatIntent.RECEIVED_BIZUM),
        )

    if "bizum" in text:
        return IntentDecision(
            intent=ChatIntent.RECENT_BIZUM,
            confidence=0.85,
            reason="Detected generic Bizum request",
            tool_name=_get_tool_name_for_intent(ChatIntent.RECENT_BIZUM),
        )

    return IntentDecision(
        intent=ChatIntent.FALLBACK,
        confidence=0.40,
        reason="No clear banking intent detected by rules",
        tool_name=_get_tool_name_for_intent(ChatIntent.FALLBACK),
    )

def detect_intent(message: str) -> ChatIntent:
    decision = classify_intent(message)

    if decision.confidence < 0.6:
        decision = detect_intent_rule_based(message)

    return decision.intent

def _get_entity_value(decision: IntentDecision, name: str) -> str | None:
    for entity in decision.entities:
        entity_name = entity.name if hasattr(entity, "name") else entity.get("name")
        if entity_name == name:
            normalized_value = (
                entity.normalized_value
                if hasattr(entity, "normalized_value")
                else entity.get("normalized_value")
            )
            raw_value = (
                entity.value if hasattr(entity, "value") else entity.get("value")
            )
            return normalized_value or raw_value
    return None


def _compute_missing_entities(decision: IntentDecision) -> list[str]:
    """
    Devuelve qué entidades requeridas por el intent no están presentes
    en decision.entities.
    """
    intent = decision.intent
    required = _get_required_entities(intent)

    missing: list[str] = []
    for entity_name in required:
        if _get_entity_value(decision, entity_name) is None:
            missing.append(entity_name)

    return missing


def _serialize_entities(decision: IntentDecision) -> list[dict]:
    serialized = []
    for entity in decision.entities:
        if hasattr(entity, "model_dump"):
            serialized.append(entity.model_dump())
        else:
            serialized.append(entity)
    return serialized


def _save_chat_message(
    session: Session,
    session_id: str,
    user_id: str,
    role: str,
    content: str,
    intent: str | None = None,
    tool_name: str | None = None,
    needs_clarification: bool = False,
    clarification_question: str | None = None,
    entities: list[dict] | None = None,
    missing_entities: list[str] | None = None,
    decision_reason: str | None = None,
    decision_confidence: float | None = None,
) -> None:
    message = ChatMessage(
        session_id=session_id,
        user_id=user_id,
        role=role,
        content=content,
        intent=intent,
        tool_name=tool_name,
        needs_clarification=needs_clarification,
        clarification_question=clarification_question,
        entities_json=json.dumps(entities) if entities is not None else None,
        missing_entities_json=json.dumps(missing_entities)
        if missing_entities is not None
        else None,
        decision_reason=decision_reason,
        decision_confidence=decision_confidence,
    )
    session.add(message)
    session.commit()


def _get_pending_clarification(
    session: Session,
    session_id: str,
    user_id: str,
) -> ChatMessage | None:
    return session.exec(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .where(ChatMessage.user_id == user_id)
        .where(ChatMessage.role == "assistant")
        .where(ChatMessage.needs_clarification)
        .order_by(ChatMessage.created_at.desc())
    ).first()


def _resolve_account_alias_from_message(
    session: Session,
    user_id: str,
    message: str,
) -> str | None:
    normalized_message = _normalize_text(message)
    accounts = get_public_accounts_by_user_id(session, user_id)

    for account in accounts:
        if account.alias and _normalize_text(account.alias) in normalized_message:
            return account.alias

    if "cuenta " in normalized_message:
        candidate = normalized_message.split("cuenta ", 1)[1].strip()
        for account in accounts:
            if account.alias and candidate in _normalize_text(account.alias):
                return account.alias

    return None


def _resolve_pending_clarification(
    session: Session,
    session_id: str,
    user_id: str,
    message: str,
) -> IntentDecision | None:
    pending = _get_pending_clarification(session, session_id, user_id)

    if not pending or not pending.missing_entities_json:
        return None

    try:
        missing_entities = json.loads(pending.missing_entities_json)
    except json.JSONDecodeError:
        return None

    if "account_alias" in missing_entities:
        resolved_alias = _resolve_account_alias_from_message(session, user_id, message)

        if resolved_alias:
            return IntentDecision(
                intent=ChatIntent(pending.intent),
                confidence=0.95,
                reason="Resolved account_alias from clarification turn",
                tool_name=pending.tool_name,
                needs_clarification=False,
                clarification_question=None,
                missing_entities=[],
                entities=[
                    {
                        "name": "account_alias",
                        "value": resolved_alias,
                        "normalized_value": _normalize_text(resolved_alias),
                    }
                ],
            )

    return None


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

    decision = _resolve_pending_clarification(
        session=session,
        session_id=session_id,
        user_id=user_id,
        message=message,
    )

    if decision is None:
        decision = classify_intent(message)

    if decision.confidence < 0.6:
        decision = detect_intent_rule_based(message)

    intent = decision.intent
    normalized_message = _normalize_text(message)

    missing_entities = _compute_missing_entities(decision)

    if (
        intent in {ChatIntent.BALANCE_SUMMARY, ChatIntent.RECENT_TRANSACTIONS}
        and "cuenta" in normalized_message
        and _get_entity_value(decision, "account_alias") is None
    ):
        decision.needs_clarification = True
        decision.missing_entities = ["account_alias"]
        decision.clarification_question = (
            "¿De qué cuenta quieres ver la información?"
            if intent == ChatIntent.BALANCE_SUMMARY
            else "¿De qué cuenta quieres ver los movimientos?"
        )
        decision.reason = "The user asked about account-specific information but did not provide account_alias."
    else:
        decision.needs_clarification = False
        decision.missing_entities = missing_entities

    if decision.needs_clarification:
        response = ChatResponse(
            answer=decision.clarification_question
            or "Necesito un poco más de información para ayudarte.",
            intent=intent,
            data={
                "entities": _serialize_entities(decision),
                "missing_entities": decision.missing_entities,
                "reason": decision.reason,
                "confidence": decision.confidence,
                "tool_name": decision.tool_name,
            },
            suggestions=[],
            ui_hints={"component": "clarification_message"},
            tools_used=[],
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
            intent=decision.intent.value,
            tool_name=_get_tool_name_for_intent(intent),
            needs_clarification=decision.needs_clarification,
            clarification_question=decision.clarification_question,
            entities=_serialize_entities(decision),
            missing_entities=decision.missing_entities,
            decision_reason=decision.reason,
            decision_confidence=decision.confidence,
        )
        return response

    if intent == ChatIntent.BALANCE_SUMMARY:
        account_alias = _get_entity_value(decision, "account_alias")

        if account_alias:
            accounts = get_public_accounts_by_user_id(session, user_id)

            matched_account = next(
                (
                    acc
                    for acc in accounts
                    if acc.alias and account_alias in acc.alias.lower()
                ),
                None,
            )

            if matched_account:
                response = ChatResponse(
                    answer=(
                        f"El saldo de tu cuenta {matched_account.alias} es "
                        f"{matched_account.balance} {matched_account.currency}."
                    ),
                    intent=intent,
                    data={
                        "account_id": matched_account.account_id,
                        "alias": matched_account.alias,
                        "balance": matched_account.balance,
                        "currency": matched_account.currency,
                    },
                    suggestions=[
                        ChatSuggestion(
                            id="accounts_list",
                            label="Ver todas mis cuentas",
                            prompt="Muéstrame mis cuentas",
                            kind="chip",
                            category="accounts",
                        ),
                        ChatSuggestion(
                            id="balance_summary_total",
                            label="Saldo total",
                            prompt="¿Cuál es mi saldo total?",
                            kind="chip",
                            category="accounts",
                        ),
                    ],
                    ui_hints={"component": "balance_summary_card"},
                    tools_used=["get_accounts"],
                )

                _save_chat_message(
                    session=session,
                    session_id=session_id,
                    user_id=user_id,
                    role="assistant",
                    content=response.answer,
                    intent=decision.intent.value,
                    tool_name=_get_tool_name_for_intent(intent),
                    needs_clarification=False,
                    clarification_question=None,
                    entities=_serialize_entities(decision),
                    missing_entities=decision.missing_entities,
                    decision_reason=decision.reason,
                    decision_confidence=decision.confidence,
                )
                return response

        summary = get_detailed_balance_summary_by_user_id(session, user_id)

        response = ChatResponse(
            answer=(
                f"Tienes un saldo total de {summary.total_balance} {summary.currency} "
                f"repartido en {summary.account_count} cuentas."
            ),
            intent=intent,
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
            ui_hints={"component": "balance_summary_card"},
            tools_used=["get_balance_summary"],
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
            intent=decision.intent.value,
            tool_name=_get_tool_name_for_intent(intent),
            needs_clarification=False,
            clarification_question=None,
            entities=_serialize_entities(decision),
            missing_entities=decision.missing_entities,
            decision_reason=decision.reason,
            decision_confidence=decision.confidence,
        )
        return response

    if intent == ChatIntent.ACCOUNTS:
        accounts = get_public_accounts_by_user_id(session, user_id)

        if not accounts:
            response = ChatResponse(
                answer="No he encontrado cuentas asociadas a tu usuario.",
                intent=intent,
                data={"accounts": [], "count": 0},
                suggestions=[
                    ChatSuggestion(
                        id="balance_summary",
                        label="Ver saldo total",
                        prompt="¿Cuál es mi saldo total?",
                        kind="chip",
                        category="accounts",
                    )
                ],
                ui_hints={"component": "account_list"},
                tools_used=["get_accounts"],
            )

            _save_chat_message(
                session=session,
                session_id=session_id,
                user_id=user_id,
                role="assistant",
                content=response.answer,
                intent=decision.intent.value,
                tool_name=_get_tool_name_for_intent(intent),
                needs_clarification=False,
                clarification_question=None,
                entities=_serialize_entities(decision),
                missing_entities=decision.missing_entities,
                decision_reason=decision.reason,
                decision_confidence=decision.confidence,
            )
            return response

        account_lines = [
            f"- {acc.alias}: {acc.balance} {acc.currency}" for acc in accounts
        ]

        response = ChatResponse(
            answer="Estas son tus cuentas:\n" + "\n".join(account_lines),
            intent=intent,
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
            ui_hints={"component": "account_list"},
            tools_used=["get_accounts"],
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
            intent=decision.intent.value,
            tool_name=_get_tool_name_for_intent(intent),
            needs_clarification=False,
            clarification_question=None,
            entities=_serialize_entities(decision),
            missing_entities=decision.missing_entities,
            decision_reason=decision.reason,
            decision_confidence=decision.confidence,
        )
        return response

    if intent == ChatIntent.RECENT_TRANSACTIONS:
        account_alias = _get_entity_value(decision, "account_alias")
        tx_response = get_public_transactions_by_user_id(
            session,
            user_id,
            limit=5,
            account_alias=account_alias,
        )

        if not tx_response.items:
            response = ChatResponse(
                answer="No he encontrado movimientos recientes.",
                intent=intent,
                data={"items": [], "count": 0},
                suggestions=[
                    ChatSuggestion(
                        id="accounts_list",
                        label="Ver cuentas",
                        prompt="Muéstrame mis cuentas",
                        kind="chip",
                        category="accounts",
                    )
                ],
                ui_hints={"component": "transaction_list"},
                tools_used=["get_recent_transactions"],
            )

            _save_chat_message(
                session=session,
                session_id=session_id,
                user_id=user_id,
                role="assistant",
                content=response.answer,
                intent=decision.intent.value,
                tool_name=_get_tool_name_for_intent(intent),
                needs_clarification=False,
                clarification_question=None,
                entities=_serialize_entities(decision),
                missing_entities=decision.missing_entities,
                decision_reason=decision.reason,
                decision_confidence=decision.confidence,
            )
            return response

        lines = [
            f"- {tx.booking_date}: {tx.description} ({tx.amount} {tx.currency})"
            for tx in tx_response.items
        ]

        response = ChatResponse(
            answer="Estos son tus últimos movimientos:\n" + "\n".join(lines),
            intent=intent,
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
            ui_hints={"component": "transaction_list"},
            tools_used=["get_recent_transactions"],
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
            intent=decision.intent.value,
            tool_name=_get_tool_name_for_intent(intent),
            needs_clarification=False,
            clarification_question=None,
            entities=_serialize_entities(decision),
            missing_entities=decision.missing_entities,
            decision_reason=decision.reason,
            decision_confidence=decision.confidence,
        )
        return response

    if intent == ChatIntent.RECENT_BIZUM:
        bizum_response = get_public_bizum_events_by_user_id(session, user_id, limit=5)

        if not bizum_response.items:
            response = ChatResponse(
                answer="No he encontrado actividad reciente de Bizum.",
                intent=intent,
                data={"items": [], "count": 0},
                suggestions=[
                    ChatSuggestion(
                        id="recent_transactions",
                        label="Ver movimientos",
                        prompt="Muéstrame mis últimos movimientos",
                        kind="chip",
                        category="transactions",
                    )
                ],
                ui_hints={"component": "bizum_list"},
                tools_used=["get_recent_bizum"],
            )

            _save_chat_message(
                session=session,
                session_id=session_id,
                user_id=user_id,
                role="assistant",
                content=response.answer,
                intent=decision.intent.value,
                tool_name=_get_tool_name_for_intent(intent),
                needs_clarification=False,
                clarification_question=None,
                entities=_serialize_entities(decision),
                missing_entities=decision.missing_entities,
                decision_reason=decision.reason,
                decision_confidence=decision.confidence,
            )
            return response

        lines = [
            f"- {event.booking_date}: {event.direction} {event.amount} {event.currency} con {event.counterparty}"
            for event in bizum_response.items
        ]

        response = ChatResponse(
            answer="Esta es tu actividad reciente de Bizum:\n" + "\n".join(lines),
            intent=intent,
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
            ui_hints={"component": "bizum_list"},
            tools_used=["get_recent_bizum"],
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
            intent=decision.intent.value,
            tool_name=_get_tool_name_for_intent(intent),
            needs_clarification=False,
            clarification_question=None,
            entities=_serialize_entities(decision),
            missing_entities=decision.missing_entities,
            decision_reason=decision.reason,
            decision_confidence=decision.confidence,
        )
        return response

    if intent == ChatIntent.RECEIVED_BIZUM:
        bizum_response = get_received_bizum_events_by_user_id(
            session,
            user_id,
            limit=5,
        )

        if not bizum_response.items:
            response = ChatResponse(
                answer="No he encontrado Bizum recibidos recientemente.",
                intent=intent,
                data={"items": [], "count": 0},
                suggestions=[
                    ChatSuggestion(
                        id="recent_bizum",
                        label="Bizum reciente",
                        prompt="Enséñame mi actividad reciente de Bizum",
                        kind="chip",
                        category="bizum",
                    )
                ],
                ui_hints={"component": "bizum_list"},
                tools_used=["get_received_bizum"],
            )

            _save_chat_message(
                session=session,
                session_id=session_id,
                user_id=user_id,
                role="assistant",
                content=response.answer,
                intent=decision.intent.value,
                tool_name=_get_tool_name_for_intent(intent),
                needs_clarification=False,
                clarification_question=None,
                entities=_serialize_entities(decision),
                missing_entities=decision.missing_entities,
                decision_reason=decision.reason,
                decision_confidence=decision.confidence,
            )
            return response

        lines = [
            f"- {event.booking_date}: {event.amount} {event.currency} de {event.counterparty}"
            for event in bizum_response.items
        ]

        response = ChatResponse(
            answer="Estos son tus últimos Bizum recibidos:\n" + "\n".join(lines),
            intent=intent,
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
            ui_hints={"component": "bizum_list"},
            tools_used=["get_received_bizum"],
        )

        _save_chat_message(
            session=session,
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response.answer,
            intent=decision.intent.value,
            tool_name=_get_tool_name_for_intent(intent),
            needs_clarification=False,
            clarification_question=None,
            entities=_serialize_entities(decision),
            missing_entities=decision.missing_entities,
            decision_reason=decision.reason,
            decision_confidence=decision.confidence,
        )
        return response

    response = ChatResponse(
        answer="Todavía no puedo responder a esa consulta. Por ahora prueba con saldo, cuentas, movimientos o Bizum.",
        intent=intent,
        data={
            "reason": decision.reason,
            "confidence": decision.confidence,
            "tool_name": decision.tool_name,
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
        ui_hints={"component": "fallback_message"},
        tools_used=[],
    )

    _save_chat_message(
        session=session,
        session_id=session_id,
        user_id=user_id,
        role="assistant",
        content=response.answer,
        intent=decision.intent.value,
        tool_name=_get_tool_name_for_intent(intent),
        needs_clarification=False,
        clarification_question=None,
        entities=_serialize_entities(decision),
        missing_entities=decision.missing_entities,
        decision_reason=decision.reason,
        decision_confidence=decision.confidence,
    )
    return response
