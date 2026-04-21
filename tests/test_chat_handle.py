from sqlmodel import SQLModel, Session, create_engine

from app.db.seed_accounts import seed_accounts
from app.db.seed_transactions import seed_transactions
from app.db.seed_users import seed_users
from app.schemas.chat import ChatIntent
from app.services.chat_router import handle_chat


DEMO_USER_ID = "u001"
TEST_SESSION_ID = "test-session-1"


def _build_session() -> Session:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    seed_users(session)
    seed_accounts(session)
    seed_transactions(session)
    return session


def test_handle_chat_balance_summary():
    session = _build_session()

    response = handle_chat(
        session=session,
        message="¿Cuál es mi saldo total?",
        user_id=DEMO_USER_ID,
        session_id=TEST_SESSION_ID,
    )

    assert response is not None
    assert response.intent == ChatIntent.BALANCE_SUMMARY
    assert "saldo total" in response.answer.lower()

    assert response.data is not None
    assert "total_balance" in response.data
    assert "currency" in response.data
    assert "account_count" in response.data

    assert response.ui_hints is not None
    assert response.ui_hints["component"] == "balance_summary_card"

    assert response.suggestions is not None
    assert len(response.suggestions) >= 1

    assert response.tools_used == ["get_balance_summary"]


def test_handle_chat_accounts():
    session = _build_session()

    response = handle_chat(
        session=session,
        message="Qué cuentas tengo",
        user_id=DEMO_USER_ID,
        session_id=TEST_SESSION_ID,
    )

    assert response is not None
    assert response.intent == ChatIntent.ACCOUNTS
    assert "cuentas" in response.answer.lower()

    assert response.data is not None
    assert "accounts" in response.data
    assert "count" in response.data

    assert response.ui_hints is not None
    assert response.ui_hints["component"] == "account_list"

    assert response.suggestions is not None
    assert len(response.suggestions) >= 1

    assert response.tools_used == ["get_accounts"]


def test_handle_chat_recent_transactions():
    session = _build_session()

    response = handle_chat(
        session=session,
        message="Enséñame mis últimos movimientos",
        user_id=DEMO_USER_ID,
        session_id=TEST_SESSION_ID,
    )

    assert response is not None
    assert response.intent == ChatIntent.RECENT_TRANSACTIONS
    assert "movimientos" in response.answer.lower()

    assert response.data is not None
    assert "items" in response.data
    assert "count" in response.data

    assert response.ui_hints is not None
    assert response.ui_hints["component"] == "transaction_list"

    assert response.suggestions is not None
    assert len(response.suggestions) >= 1

    assert response.tools_used == ["get_recent_transactions"]


def test_handle_chat_recent_bizum():
    session = _build_session()

    response = handle_chat(
        session=session,
        message="Quiero ver mi actividad Bizum",
        user_id=DEMO_USER_ID,
        session_id=TEST_SESSION_ID,
    )

    assert response is not None
    assert response.intent == ChatIntent.RECENT_BIZUM
    assert "bizum" in response.answer.lower()

    assert response.data is not None
    assert "items" in response.data
    assert "count" in response.data

    assert response.ui_hints is not None
    assert response.ui_hints["component"] == "bizum_list"

    assert response.suggestions is not None
    assert len(response.suggestions) >= 1

    assert response.tools_used == ["get_recent_bizum"]


def test_handle_chat_received_bizum():
    session = _build_session()

    response = handle_chat(
        session=session,
        message="He recibido algún Bizum estos días?",
        user_id=DEMO_USER_ID,
        session_id=TEST_SESSION_ID,
    )

    assert response is not None
    assert response.intent == ChatIntent.RECEIVED_BIZUM
    assert "bizum" in response.answer.lower()

    assert response.data is not None
    assert "items" in response.data
    assert "count" in response.data

    assert response.ui_hints is not None
    assert response.ui_hints["component"] == "bizum_list"

    assert response.suggestions is not None
    assert len(response.suggestions) >= 1

    assert response.tools_used == ["get_received_bizum"]


def test_handle_chat_fallback():
    session = _build_session()

    response = handle_chat(
        session=session,
        message="quiero pedir una hipoteca",
        user_id=DEMO_USER_ID,
        session_id=TEST_SESSION_ID,
    )

    assert response is not None
    assert response.intent == ChatIntent.FALLBACK
    assert response.answer is not None
    assert len(response.answer) > 0

    assert response.data is not None
    assert "reason" in response.data
    assert "confidence" in response.data
    assert "tool_name" in response.data

    assert response.suggestions is not None
    assert len(response.suggestions) > 0

    assert response.ui_hints is not None
    assert response.ui_hints["component"] == "fallback_message"

    assert response.tools_used == []
