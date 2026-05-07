import re
import unicodedata
import langsmith as ls
from langchain_openai import ChatOpenAI
from langsmith import traceable
from pydantic import BaseModel, Field

from app.core.config import settings
from app.schemas.chat import ChatIntent, EntityValue, IntentDecision
from app.services.chat_taxonomy import INTENT_TOOL_MAP

KNOWN_ACCOUNT_ALIASES = {
    "nomina": "Nómina",
    "ahorro": "Ahorro",
    "gastos": "Gastos",
    "principal": "Principal",
}

client = ls.Client(
    api_key=settings.langchain_api_key, api_url=settings.langchain_endpoint
)


class IntentAgentOutput(BaseModel):
    intent: ChatIntent = Field(description="Main banking intent detected")
    confidence: float = Field(
        description="Confidence score between 0.0 and 1.0",
        ge=0.0,
        le=1.0,
    )
    reason: str = Field(description="Short explanation for the decision")
    entities: list[EntityValue] = Field(default_factory=list)
    missing_entities: list[str] = Field(default_factory=list)
    needs_clarification: bool = False
    clarification_question: str | None = None


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
- If the user mentions a specific account, extract account_alias.
- If the user mentions "cuenta" but does not identify which one, request clarification.
- Do not invent entities that are not grounded in the user message.

Return structured output only.
User message:
{message}
""".strip()


def _fallback_decision(message: str, source: str) -> IntentDecision:
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
        or "movimientos" in text
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

    return IntentDecision(
        intent=intent,
        confidence=confidence,
        reason=reason,
        tool_name=INTENT_TOOL_MAP[intent],
        entities=[],
        missing_entities=[],
        needs_clarification=False,
        clarification_question=None,
        source=source,
    )


def _post_process_result(result: IntentAgentOutput) -> IntentAgentOutput:
    result.confidence = max(0.0, min(1.0, result.confidence))

    if result.intent == ChatIntent.FALLBACK:
        result.needs_clarification = False
        result.missing_entities = []
        result.clarification_question = None

    if result.clarification_question is not None:
        result.clarification_question = result.clarification_question.strip() or None

    return result


def classify_intent(message: str) -> IntentDecision:
    with ls.tracing_context(
        client=client,
        project_name="koi",
        enabled=True,
    ):
        return _classify_intent_inner(message)


@traceable(
    name="intent_agent.classify_intent",
    run_type="chain",
    tags=["koi", "intent-agent", "sprint-8"],
    project_name="koi",
)
def _classify_intent_inner(message: str) -> IntentDecision:
    try:
        llm = ChatOpenAI(
            model=settings.openai_model, temperature=0, api_key=settings.openai_api_key
        )

        structured_llm = llm.with_structured_output(IntentAgentOutput)

        result = structured_llm.invoke(build_intent_prompt(message))
        result = _post_process_result(result)

        return IntentDecision(
            intent=result.intent,
            confidence=result.confidence,
            reason=result.reason,
            tool_name=INTENT_TOOL_MAP[result.intent],
            entities=result.entities,
            missing_entities=result.missing_entities,
            needs_clarification=result.needs_clarification,
            clarification_question=result.clarification_question,
            source="llm",
        )

    except Exception:
        return _fallback_decision(message, source="fallback_error")
