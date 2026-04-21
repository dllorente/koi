# Koi

Koi is an AI banking copilot project built from scratch as a sprint-based MVP.

The name stands for **Know your Own fInances** and represents the idea of a secure, read-only banking assistant focused on authenticated personal finance queries.[cite:12]

---

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

### Sprint 3 completed
- `/chat` endpoint protected by JWT Bearer auth.[cite:300]
- `ChatIntent` enum and deterministic routing based on normalized Spanish banking queries (saldo, cuentas, movimientos, Bizum).[cite:300]
- `handle_chat` service returning structured responses with `answer`, `intent`, `data`, `suggestions` (chips) and `ui_hints` for frontend integration.[cite:300]
- Unit tests covering all main intents (saldo, cuentas, movimientos, Bizum reciente, Bizum recibidos, fallback).[cite:742]

### Sprint 4 completed
- Migration from fully mocked datasets to **real SQLite persistence** using **SQLModel** for users, accounts, transactions, Bizum events and chat messages.[web:866][web:863]
- Application startup lifecycle creating tables and seeding demo banking data automatically for local development.[web:866]
- `/chat` endpoint now persisting both user and assistant messages into `chatmessage` with `user_id`, `session_id`, `role`, `content` and `created_at`.[web:866]
- Verified end-to-end flow: `auth/login` → `auth/me` → `/chat` → messages stored in SQLite and queryable by `session_id`.[web:866]
- README / roadmap aligned to reflect the new persistence and chat history foundations.[file:710]

### Sprint 5 delivered the first production-oriented conversational banking core:
- banking taxonomy,
- structured intent classification,
- entity extraction and resolution,
- real clarification flow,
- persisted chat traces,
- deterministic validation and fallback.

---

## Tech stack

- Python.[cite:4]
- Poetry.[cite:12]
- FastAPI.[cite:4]
- Pydantic.[cite:12]
- **SQLModel + SQLite for database models and persistence.**[web:866]
- Uvicorn.[cite:12]
- PyJWT / python-jose-style JWT handling for access tokens.[web:730]

---

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
│   │       ├── bizum.py
│   │       └── chat.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── security.py
│   ├── data/
│   │   ├── users.py
│   │   ├── accounts.py
│   │   ├── transactions.py
│   │   └── bizum.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── models.py    # SQLModel definitions (User, Account, Transaction, BizumEvent, ChatMessage)
│   └── schemas/
│       ├── __init__.py
│       ├── user.py
│       ├── auth.py
│       ├── account.py
│       ├── transaction.py
│       ├── bizum.py
│       └── chat.py
├── tests/
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

[cite:12][cite:300][web:866]

---

## Run locally

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

On startup, the app will:

- create SQLite tables with SQLModel,
- seed demo users, accounts, transactions and Bizum events,
- prepare the `chatmessage` table to persist chat history.[web:866]

[cite:12][web:866]

---

## Available endpoints

### Public

```bash
GET  /health        # Health check
POST /auth/login    # Obtain JWT access token for demo user
```

[cite:12][cite:300]

### Protected (JWT Bearer)

All these endpoints expect an `Authorization: Bearer <access_token>` header containing a signed JWT created with `create_access_token(subject)`, where `subject` is typically the user identifier.[web:730][cite:698]

```bash
GET  /auth/me
GET  /accounts
GET  /accounts/summary
GET  /transactions/recent
GET  /transactions/accounts/{account_id}
GET  /bizum/recent
GET  /bizum/received
POST /chat
```

- `POST /chat`: rule-based banking chat endpoint that detects `ChatIntent` and returns structured responses (`answer`, `intent`, `data`, `suggestions`, `ui_hints`) for queries like balance, accounts, recent movements, Bizum activity, and fallback.[cite:300][cite:742]
- The chat endpoint **persists each turn** into `chatmessage` with `user_id` (from JWT), `session_id` (from request), `role` (`user` / `assistant`) and `content`, enabling conversation history queries per session.[web:866]

---

## Chat persistence model

The authentication token identifies **who** is calling the API, while `session_id` identifies **which conversation thread** the message belongs to.

Current design:

- `user_id`: resolved from the JWT and stored with each message.[web:782]
- `session_id`: provided by the client; groups messages belonging to the same conversation.[web:878]
- `role`: `"user"` or `"assistant"`.
- `content`: stored chat message text.
- `created_at`: timestamp for message ordering.

This allows the same authenticated user to hold **multiple independent chat sessions** by using different `session_id` values.

> In the current MVP, the client is responsible for generating and sending `session_id` (e.g. a UUID) when starting a new chat. A future sprint will introduce a formal `ChatSession` model and dedicated endpoints to create and list chat sessions.[web:878][cite:881]

---

## Health check

```bash
GET /health
```

Expected response:

```json
{"status": "ok"}
```

[cite:12]

---

## Notes

- Authentication uses **JWT access tokens** signed with a secret key and expiration; banking datasets (users, accounts, transactions, Bizum) are now backed by **SQLite + SQLModel** instead of pure in-memory mocks.[web:866][cite:698]
- Protected endpoints are validated by the backend via a dependency that decodes the JWT and resolves the current user; Swagger UI can be used for manual exploration, but `curl` or API clients (HTTPie, Postman) are recommended to control the `Authorization` header explicitly.[cite:34]
- Future hardening will include stronger password hashing for demo users, refined token lifetime/refresh strategies, and **formal chat session management** (backend-driven or frontend-coordinated session creation) on top of the current `session_id`-based persistence.[cite:35][web:878]

---

# Koi Roadmap

Koi evoluciona desde una API bancaria read-only hacia un **fintech copilot** con arquitectura conversacional, frontend de producto, observabilidad, seguridad y capacidades enterprise.  
El punto de inflexión principal está en **v0.5.0**, donde el sistema deja atrás el **routing ad hoc** como mecanismo principal y adopta una base conversacional guiada por **taxonomía, intent detection con LLM, resolución de entidades y aclaración multi-turno**.

| Sprint | Versión | Objetivo | Entregables clave | Valor arquitectónico |
|---|---|---|---|---|
| 1 | v0.1.0 | Base project scaffolding | Poetry, FastAPI, health check, estructura modular inicial, configuración por entorno | Base mantenible y preparada para crecer |
| 2 | v0.2.0 | Authenticated read-only banking baseline | Mock auth, demo users, `/auth/me`, cuentas, saldo, transacciones y Bizum mock | Primer contrato funcional de API bancaria read-only |
| 3 | v0.3.0 | Chat endpoint with rule-based banking routing | `/chat` protegido, `ChatIntent`, router determinista, tests unitarios | Separa intención, handlers y capa de respuesta |
| 4 | v0.4.0 | API hardening, persistence & quality | HTTPBearer/JWT, **SQLite persistence with SQLModel for banking data and chat messages**, errores robustos, tests ampliados, README y CHANGELOG | Base backend seria para evolucionar a producto |
| 5 | v0.5.0 | Conversational banking core with LLM taxonomy, intent detection, entity resolution and clarification | **Taxonomía cerrada de intents y entidades bancarias**; `intent_agent` con salida estructurada (`intent`, `confidence`, `entities`, `missing_entities`, `needs_clarification`, `tool_candidates`); tools bancarias read-only (`get_balance`, `get_accounts`, `get_recent_transactions`, `get_recent_bizum`); **entity resolution** sobre mensaje y contexto; **desambiguación multi-turno real** para respuestas de aclaración; validación determinista mínima (schema, confidence, guardrails); persistencia básica de decisiones y trazas; tests funcionales multi-turno | Primer núcleo conversacional bancario productivo: separa comprensión semántica, resolución de contexto y ejecución segura de tools, reduciendo la lógica ad hoc a validación y control |
| 6 | v0.6.0 | Professional product UI / frontend MVP | UI profesional para login, cuentas, saldo, movimientos, Bizum y chat conectado a la API | Permite demo real de producto sin depender de Swagger |
| 7 | v0.7.0 | Conversational UX, session state & persistent chat history | Historial persistente, recuperación por sesión y usuario, estado conversacional visible, continuidad de aclaraciones pendientes, mejoras de UX de chat | Introduce continuidad conversacional real y consolida el diálogo multi-turno sobre el core LLM del sprint 5 |
| 8 | v0.8.0 | Observability & evaluation foundations | Trazas end-to-end, dataset inicial de evaluación, métricas de calidad por intent, entity resolution y clarification, logging estructurado | Observability y evals pasan a medir no solo respuestas, sino también clasificación, slots y desambiguación, que son base de asistentes en producción |
| 9 | v0.9.0 | Guardrails & safe fintech interaction | Validación de inputs, control de outputs, anti prompt-injection, modo read-only reforzado, políticas seguras | Safety y guardrails separan el core conversacional funcional de un sistema fintech fiable y gobernado |
| 10 | v1.0.0 | Deployment-ready MVP | Docker, CI/CD, despliegue backend/frontend, configuración por entorno, release checklist | Koi pasa de proyecto local a MVP desplegable |
| 11 | v1.1.0 | Memory architecture & user context | Memoria corto/largo plazo, preferencias de usuario, políticas de retención y borrado | Separa memoria, perfil y contexto operativo del agente |
| 12 | v1.2.0 | Retrieval & banking knowledge layer | RAG para FAQs, políticas y glosario, retrieval refinement, grounding y evaluación de retrieval | Añade conocimiento bancario verificable al agente |
| 13 | v1.3.0 | Orchestration architecture with LangGraph | Grafo explícito, planner/router, synthesis, retries, fallbacks y branching | Arquitectura agentic observable y controlada |
| 14 | v1.4.0 | Frontend product experience | UI de producto conectada a API y agente, historial persistente visible, demo end-to-end | Convierte Koi en una experiencia de producto enseñable |
| 15 | v1.5.0 | Human-in-the-loop & approval workflows | HITL para casos ambiguos o sensibles, aprobación manual, auditoría de decisiones | Muy relevante en finanzas por control y accountability |
| 16 | v1.6.0 | Governance, auditability & compliance posture | Audit trail, redacción de datos sensibles, versionado de prompts y policies, catálogo de riesgos | Gobernanza y trazabilidad de nivel enterprise |
| 17 | v1.7.0 | Advanced evals & safety scorecards | Evals offline y online, benchmarks regresivos, edge cases financieros, scorecards por tool e intent | Permite medir calidad, seguridad y regresiones |
| 18 | v1.8.0 | Multi-model strategy & cost-performance routing | Routing entre modelos por coste, latencia y calidad, fallback entre proveedores, telemetría de coste | Arquitectura moderna optimizada para producción |
| 19 | v1.9.0 | Platformization & external integrations | API madura, integraciones externas, capacidades tipo MCP y contracts de tools | Prepara Koi para ecosistemas multi-agente |
| 20 | v2.0.0 | Enterprise-grade fintech copilot showcase | Demo estable end-to-end, arquitectura documentada, casos de uso de negocio, storytelling técnico | Posiciona Koi como portfolio senior de AI Engineer / Solutions Architect |


[cite:300]

---

## Lectura por etapas

- **v0.x**: construcción del producto funcional, desde API bancaria autenticada hasta routing agentic inicial y primera UI usable.[cite:300]  
- **v1.x**: maduración como sistema agentic serio, con memoria, RAG, observabilidad, guardrails, human-in-the-loop y gobernanza.[cite:300]  
- **v2.0**: consolidación como showcase enterprise orientado a portfolio senior, con arquitectura y demo de producto completas.[cite:300]

---

## Capacidades arquitectónicas cubiertas

- Seguridad básica y auth seria con Bearer + JWT (ya implementado a nivel de generación y validación de tokens para usuarios demo).[cite:698]
- Persistencia real y separación entre API, datos, memoria y experiencia de usuario (introducida progresivamente a partir de Sprint 4 con SQLite + SQLModel para datos bancarios y chat). [web:866][cite:300]
- Routing híbrido y posterior evolución a orquestación agentic con tools.[cite:300]
- Observabilidad, evaluación y guardrails como base de fiabilidad operativa.[cite:300]
- Human-in-the-loop, auditabilidad y gobierno del sistema para contexto fintech.[cite:300]
- Estrategia multi-modelo y preparación para integraciones externas y ecosistemas más amplios.[cite:300]