import requests


BASE_URL = "http://127.0.0.1:8000"


def login(email: str, password: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_me(access_token: str) -> dict:
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def send_chat_message(access_token: str, message: str, session_id: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/chat",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "message": message,
            "session_id": session_id,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
