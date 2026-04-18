from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.accounts import router as accounts_router
from app.api.routes.transactions import router as transactions_router
from app.api.routes.bizum import router as bizum_router
from app.api.routes.chat import router as chat_router


#Creamos la app FastAPI.
app= FastAPI(
    title = "Koi API",
    version = "0.3.0",
    description ="Authenticated banking copilot MVP"
)

#endpoint mínimo para saber que esta vivo el proyecto
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(bizum_router)
app.include_router(chat_router)
