import pytest

from app.schemas.chat import ChatIntent
from app.services.chat_router import detect_intent

@pytest.mark.parametrize(
    "message,expected_intent",
    [
        ("Qué cuentas tengo", ChatIntent.ACCOUNTS),
        ("Mis cuentas", ChatIntent.ACCOUNTS),
        ("cuentas", ChatIntent.ACCOUNTS),
    ]
)

def test_detect_intent_accounts(message, expected_intent):
    assert detect_intent(message) == expected_intent


@pytest.mark.parametrize(
    "message,expected_intent",
    [
        ("Enséñame mis últimos movimientos", ChatIntent.RECENT_TRANSACTIONS),
        ("Quiero ver movimientos recientes", ChatIntent.RECENT_TRANSACTIONS),
        ("Muéstrame mis gastos recientes", ChatIntent.RECENT_TRANSACTIONS),
    ],
)

def test_detect_intent_transactions(message, expected_intent):
    assert detect_intent(message) == expected_intent


@pytest.mark.parametrize(
    "message,expected_intent",
    [
        ("He recibido algún Bizum estos días?", ChatIntent.RECEIVED_BIZUM),
        ("Bizum recibidos", ChatIntent.RECEIVED_BIZUM),
    ],
)

def test_detect_intent_bizum_received(message, expected_intent):
    assert detect_intent(message) == expected_intent


@pytest.mark.parametrize(
    "message,expected_intent",
    [
        ("Quiero ver mi actividad Bizum", ChatIntent.RECENT_BIZUM),
        ("Bizum", ChatIntent.RECENT_BIZUM),
    ],
)

def test_detect_intent_bizum_recent(message, expected_intent):
    assert detect_intent(message) == expected_intent


def test_detect_intent_fallback():
    message = "Explícame qué es una hipoteca a tipo fijo"
    assert detect_intent(message) == ChatIntent.FALLBACK