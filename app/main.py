from sys import version
from fastapi import FastAPI

#Creamos la app FastAPI.
app= FastAPI(
    title = "Koi API",
    version = "0.1.0",
    description ="Authenticated banking copilot MVP"
)

#endpoint mínimo para saber que esta vivo el proyecto
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}