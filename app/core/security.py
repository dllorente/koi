from app.data.users import DEMO_USERS

def authenticate_user(email: str , password: str) -> dict | None:
    for user in DEMO_USERS:
        if user["email"] == email and user["password"] == password:
            return user
    return None

def create_mock_token(user_id: str) -> str:
    return f"mock-token-{user_id}"

def parse_mock_token(token: str) -> str | None:
    prefix = "mock-token-"
    if not token.startswith(prefix):
        return None
    return token.removeprefix(prefix)

def get_user_by_id(user_id: str):
    for user in DEMO_USERS:
        if user["user_id"] == user_id:
            return user
    return None