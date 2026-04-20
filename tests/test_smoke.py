from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_health():
    res = client.get("/health")  # o la ruta que tengas tipo ping
    assert res.status_code == 200

def test_smoke(client):
    res = client.get("/docs")
    assert res.status_code == 200