from app.schemas.chat import ChatIntent
from app.services.chat_router import handle_chat


# Suponemos que existe el usuario demo "u001" en tus datasets mock
DEMO_USER_ID = "u001"


def test_handle_chat_balance_summary():
    answer, intent = handle_chat("¿Cuál es mi saldo total?", DEMO_USER_ID)
    assert intent == ChatIntent.BALANCE_SUMMARY
    assert "saldo total" in answer.lower()


def test_handle_chat_accounts():
    answer, intent = handle_chat("Qué cuentas tengo", DEMO_USER_ID)
    assert intent == ChatIntent.ACCOUNTS
    # debería listar al menos una cuenta en formato "- alias: saldo moneda"
    assert "tus cuentas" in answer.lower() or "-" in answer


def test_handle_chat_recent_transactions():
    answer, intent = handle_chat("Enséñame mis últimos movimientos", DEMO_USER_ID)
    assert intent == ChatIntent.RECENT_TRANSACTIONS
    assert "últimos movimientos" in answer.lower() or "-" in answer


def test_handle_chat_recent_bizum():
    answer, intent = handle_chat("Quiero ver mi actividad Bizum", DEMO_USER_ID)
    assert intent == ChatIntent.RECENT_BIZUM
    assert "bizum" in answer.lower()


def test_handle_chat_received_bizum():
    answer, intent = handle_chat("He recibido algún Bizum estos días?", DEMO_USER_ID)
    assert intent == ChatIntent.RECEIVED_BIZUM
    assert "bizum" in answer.lower()


def test_handle_chat_fallback():
    answer, intent = handle_chat("Explícame qué es una hipoteca a tipo fijo", DEMO_USER_ID)
    assert intent == ChatIntent.FALLBACK
    assert "todavía no puedo responder" in answer.lower()