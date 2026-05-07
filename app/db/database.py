from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from app.core.settings import settings


def _ensure_sqlite_directory(database_url: str) -> None:
    sqlite_prefix = "sqlite:///"
    if database_url.startswith(sqlite_prefix):
        db_path = database_url.removeprefix(sqlite_prefix)
        path = Path(db_path)
        if path.parent:
            path.parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_directory(settings.database_url)

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args=connect_args,
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
