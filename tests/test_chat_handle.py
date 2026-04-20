from sqlmodel import SQLModel, Session, create_engine

from app.services.chat_router import handle_chat, ChatIntent
from app.db.seed_users import seed_users
from app.db.seed_accounts import seed_accounts
from app.db.seed_transactions import seed_transactions
from types import SimpleNamespace

test_user = SimpleNamespace(
    id=1,
    user_id="u001",
    email="demo@example.com",
    full_name="Demo User",
    session_id="test-session-1"
)
DEMO_USER_ID = "u001"  # o el user_id que tengas en tu seed
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
    result = handle_chat(session, "¿Cuál es mi saldo total?", DEMO_USER_ID,TEST_SESSION_ID)

    assert result.intent == ChatIntent.BALANCE_SUMMARY.value
    assert "saldo total" in result.answer.lower()
    assert result.data is not None
    assert "total_balance" in result.data


def test_handle_chat_accounts():
    session = _build_session()
    result = handle_chat(session, "Qué cuentas tengo", DEMO_USER_ID,TEST_SESSION_ID)

    assert result.intent == ChatIntent.ACCOUNTS.value
    assert "tus cuentas" in result.answer.lower() or "-" in result.answer
    assert result.data is not None
    assert "accounts" in result.data
    

def test_handle_chat_recent_transactions():
    session = _build_session()
    result = handle_chat(session, "Enséñame mis últimos movimientos", DEMO_USER_ID,TEST_SESSION_ID)

    assert result.intent == ChatIntent.RECENT_TRANSACTIONS.value
    assert "últimos movimientos" in result.answer.lower() or "-" in result.answer
    assert result.data is not None
    assert "items" in result.data


def test_handle_chat_recent_bizum():
    session = _build_session()
    result = handle_chat(session, "Quiero ver mi actividad Bizum", DEMO_USER_ID,TEST_SESSION_ID)

    assert result.intent == ChatIntent.RECENT_BIZUM.value
    assert "bizum" in result.answer.lower()
    assert result.data is not None
    assert "items" in result.data


def test_handle_chat_received_bizum():
    session = _build_session()
    result = handle_chat(session, "He recibido algún Bizum estos días?", DEMO_USER_ID,TEST_SESSION_ID)

    assert result.intent == ChatIntent.RECEIVED_BIZUM.value
    assert "bizum" in result.answer.lower()
    assert result.data is not None
    assert "items" in result.data


def test_handle_chat_fallback():
    session = _build_session()
    response = handle_chat(session, "quiero pedir una hipoteca", DEMO_USER_ID, TEST_SESSION_ID)

    assert response.intent == ChatIntent.FALLBACK
    assert response.answer is not None
    assert len(response.answer) > 0
    assert response.suggestions is not None
    assert len(response.suggestions) > 0
  