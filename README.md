# Koi

Koi is an AI banking copilot project built from scratch as a sprint-based MVP.

## Current status
Sprint 1 completed:
- Poetry-based project setup
- FastAPI base application
- Health check endpoint
- Initial repository structure
- Semantic versioning and project documentation initialized

## Tech stack
- Python
- Poetry
- FastAPI
- Pydantic
- Uvicorn

## Project structure
```bash
koi/
├── app/
│   ├── __init__.py
│   └── main.py
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

## Health check
```bash
GET /health
```

Expected response:
```json
{"status": "ok"}
```

## Roadmap
- Sprint 1: base project scaffolding
- Sprint 2: mock authentication and demo users
- Sprint 3: accounts and balances
- Sprint 4: transactions and Bizum activity
- Sprint 5: chat orchestration with banking tools