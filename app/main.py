from fastapi import FastAPI
from sqlmodel import Session
from contextlib import asynccontextmanager

from app.api.routes.auth import router as auth_router
from app.api.routes.accounts import router as accounts_router
from app.api.routes.transactions import router as transactions_router
from app.api.routes.bizum import router as bizum_router
from app.api.routes.chat import router as chat_router


from app.db.database import create_db_and_tables, engine
from app.db.seed_users import seed_users
from app.db.seed_accounts import seed_accounts
from app.db.seed_transactions import seed_transactions
from app.db.seed_bizum import seed_bizum


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        seed_users(session)
        seed_accounts(session)
        seed_transactions(session)
        seed_bizum(session)
    yield


app = FastAPI(
    title="Koi API",
    version="0.4.0",
    description="Authenticated banking copilot MVP",
    lifespan=lifespan,
)


# endpoint mínimo para saber que esta vivo el proyecto
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(bizum_router)
app.include_router(chat_router)
