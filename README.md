# Koi

Koi is an AI banking copilot project built from scratch as a sprint-based MVP.

The name stands for **Know your Own fInances** and represents the idea of a secure, read-only banking assistant focused on authenticated personal finance queries.[cite:12]

## Current status

### Sprint 1 completed
- Poetry-based project setup.[cite:12]
- FastAPI base application.[cite:12]
- Health check endpoint.[cite:12]
- Initial repository structure.[cite:12]
- Semantic versioning and initial project documentation.[cite:12]

### Sprint 2 completed
- Mock authentication flow with demo users.[cite:12]
- Protected user resolution based on Bearer token.[cite:34]
- Authenticated `/auth/me` endpoint.[cite:34]
- Mock accounts dataset linked to authenticated users.[cite:12]
- `/accounts` endpoint for authenticated account listing.[cite:12]
- `/accounts/summary` endpoint for consolidated balance summary.[cite:12]
- Mock transactions dataset and recent transaction queries.[cite:12]
- `/transactions/recent` endpoint for authenticated recent activity.[cite:12]
- `/transactions/accounts/{account_id}` endpoint with ownership validation.[cite:12][cite:34]
- Mock Bizum dataset and user activity queries.[cite:12]
- `/bizum/recent` and `/bizum/received` endpoints.[cite:12]
- Refactor from `models/` to `schemas/` for Pydantic API contracts.[cite:60]

## Tech stack
- Python.[cite:4]
- Poetry.[cite:12]
- FastAPI.[cite:4]
- Pydantic.[cite:12]
- Uvicorn.[cite:12]

## Project structure
```bash
koi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── accounts.py
│   │       ├── transactions.py
│   │       └── bizum.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── security.py
│   ├── data/
│   │   ├── users.py
│   │   ├── accounts.py
│   │   ├── transactions.py
│   │   └── bizum.py
│   └── schemas/
│       ├── __init__.py
│       ├── user.py
│       ├── auth.py
│       ├── account.py
│       ├── transaction.py
│       └── bizum.py
├── tests/
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

## Run locally
```bash
poetry install
poetry run uvicorn app.main:app --reload
```

## Available endpoints

### Public
```bash
GET /health
POST /auth/login
```

### Protected
```bash
GET /auth/me
GET /accounts
GET /accounts/summary
GET /transactions/recent
GET /transactions/accounts/{account_id}
GET /bizum/recent
GET /bizum/received
```

## Health check
```bash
GET /health
```

Expected response:
```json
{"status": "ok"}
```

## Notes
- Authentication is currently mock-based and intended for MVP development only.[cite:35][cite:12]
- Protected endpoints are validated correctly by the backend; Swagger UI may not send the manual `Authorization` header reliably with the current implementation, so `curl` is the preferred validation method at this stage.[cite:34]
- Future hardening will include HTTPBearer, password hashing, and stronger token handling.[cite:35]

## Roadmap
- Sprint 1: base project scaffolding.[cite:12]
- Sprint 2: authenticated read-only banking baseline.[cite:12]
- Sprint 3: chat orchestration with banking tools.[cite:12]
- Sprint 4: persistence, testing, and API hardening.[cite:35][cite:34]
- Sprint 5: richer product capabilities and security improvements.[cite:35]