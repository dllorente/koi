import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from app.db.database import get_session
from app.main import app
from app.db.seed_users import seed_users
from app.db.seed_accounts import seed_accounts
from app.db.seed_transactions import seed_transactions


@pytest.fixture(name="engine")
def engine_fixture():
    # BD de test en memoria
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        # seed inicial para tests
        seed_users(session)
        seed_accounts(session)
        seed_transactions(session)
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    TestClient con get_session overrideado para usar la sesión de test.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()