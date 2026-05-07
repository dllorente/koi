# Changelog - Koi

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.7.0] - 2026-05-07

### Added
- Modelo `ChatSession` con persistencia en SQLite para gestionar sesiones de chat por usuario.
- Endpoints `GET /chat/sessions` y `GET /chat/sessions/{session_id}/messages` para listar sesiones y recuperar el historial de mensajes de una sesión.
- Títulos automáticos de sesión generados a partir del primer mensaje del usuario, con fallback a un nombre genérico cuando el texto está vacío.
- Sidebar en la UI de Streamlit con listado de sesiones, selector y botón para cargar el historial de una sesión guardada.
- Integración de los metadatos del asistente (`intent`, `tools_used`, `needs_clarification`, `decision_confidence`, `decision_reason`) en el historial al recargar una sesión.

### Changed
- Flujo de creación de sesión: el frontend usa `session_id = "default"` solo como marcador inicial y adopta el `session_id` real devuelto por el backend tras el primer mensaje.
- Esquemas de respuesta de FastAPI para sesiones y mensajes (`ChatSessionResponse`, `ChatMessageResponse`) tipados con `datetime` y configurados con `from_attributes=True` para serialización correcta.

### Fixed
- Errores de validación de respuesta (`ResponseValidationError`) en los endpoints de sesiones y mensajes causados por tipos incorrectos (`str` vs `datetime`) y campos requeridos no presentes (`session_id` en mensajes).
- Desincronización entre el estado de sesiones en la UI y el backend, asegurando ahora que el selector muestre las sesiones reales y cargue el historial correcto.

## [0.6.0] - 2026-05-03
### Added
- Conversational banking UI for interactive testing of multi-turn chat flows.
- Session-aware chat view with message history and suggestion chips.
- Debug panel to inspect detected intent, entities, missing entities, confidence and tools used.
- Faster manual validation workflow for balance, accounts, transactions and Bizum use cases.

## [0.5.0] - 2026-04-21
### Added
- Closed banking taxonomy for intents, tools and entities.
- `intent_agent` with structured output including intent, confidence, entities, missing entities and clarification signals.
- Read-only banking tools for balance summary, account listing, recent transactions and Bizum activity.
- Entity resolution over current user message and available banking context.
- Real multi-turn clarification flow for ambiguous account-specific requests.
- Persistence of chat decisions and assistant traces in database.
- Functional support for account alias disambiguation in transaction and balance queries.
### Changed
- Refactored chat routing to separate taxonomy, intent detection, clarification resolution and tool execution concerns.
- Reduced ad hoc logic in the conversational flow and moved tool naming to taxonomy mapping.
- Improved transaction retrieval to support filtering by resolved `account_alias`.### Fixed
- Fixed incorrect tool trace persistence for non-balance intents.
- Fixed clarification flow so follow-up responses such as "de la cuenta ahorro" resolve correctly.
- Fixed account-specific recent transactions so they return filtered results instead of aggregated data.

## [0.4.0] - 2026-04-20
### Added
- Real SQLite persistence with SQLModel for users, accounts, transactions, Bizum events and chat messages.
- Persisted chat conversations using `session_id`, `user_id`, `role`, `content` and `created_at`.
- Bizum endpoints backed by database queries instead of in-memory mock data.
### Changed
- Refactored chat flow to use real persistence-backed data sources for accounts, transactions and Bizum.
- Startup lifecycle now creates tables and seeds demo data through FastAPI lifespan.
### Fixed
- Resolved missing table issues for new SQLModel entities.
- Fixed schema alignment issues between DB date fields and Pydantic response models.
### Next
- Add formal `ChatSession` management and automatic `session_id` generation from frontend or backend session endpoints.
- Add chat history retrieval endpoints for persisted conversations.

## [0.3.0] - 2026-04-18
### Added
- Protected `/chat` endpoint for authenticated banking conversations.
- `ChatIntent` enum and chat schemas (`ChatRequest`, `ChatResponse`).
- Rule-based banking router for balance, accounts, recent transactions, and Bizum activity.
- Unit tests for `detect_intent()` and `handle_chat()`.
- `/tests/recent` test_smoke.py
- docker fixes to ci pipeline in github actions
### Notes
- Current intent routing is deterministic and explicitly marked as temporary.
- Future versions will replace it with agent-based LLM intent routing.
### Planned
- HTTPBearer integration for Swagger-friendly authentication flow.[cite:35]
- Password hashing with bcrypt or equivalent.[cite:35]
- Stronger token strategy beyond mock tokens.[cite:35]
- Masked IBAN exposure and richer balance modeling.[cite:12]
- Chat orchestration with internal banking tools.[cite:12]

## [0.2.0] - 2026-04-17
### Added
- Mock authentication flow with demo users.[cite:12]
- Bearer-token-based current user resolution for protected endpoints.[cite:34]
- `/auth/me` endpoint for authenticated user identity lookup.[cite:34]
- Mock accounts dataset associated with demo users.[cite:12]
- `/accounts` endpoint to list authenticated user accounts.[cite:12]
- `/accounts/summary` endpoint with consolidated balance view.[cite:12]
- Mock transactions dataset for authenticated banking activity.[cite:12]
- `/transactions/recent` endpoint for recent user transactions.[cite:12]
- `/transactions/accounts/{account_id}` endpoint for account-specific transactions.[cite:12]
- Ownership validation for account transaction access.[cite:34]
- Mock Bizum dataset for demo peer-to-peer payment activity.[cite:12]
- `/bizum/recent` endpoint for recent Bizum activity.[cite:12]
- `/bizum/received` endpoint for received Bizum events.[cite:12]

### Changed
- Project structure evolved from initial scaffold to a domain-based API layout.[cite:12]
- Pydantic API contracts were reorganized from `models/` to `schemas/`.[cite:60]

### Notes
- Protected endpoints are currently best validated with `curl` because Swagger UI may not reliably send the manual `Authorization` header in the current MVP auth approach.[cite:34]

## [0.1.0] - 2026-04-17
### Added
- Initial project scaffold created with Poetry.[cite:12]
- Base Python package structure for the Koi backend.[cite:12]
- FastAPI application bootstrap with main entrypoint.[cite:12]
- Health check endpoint for basic service validation.[cite:12]
- Initial environment configuration with `.env` support.[cite:12]
- Base `.gitignore` for Python, virtualenv, cache files, and generated artifacts.[cite:12]
- Initial `README.md` and `CHANGELOG.md` files.[cite:12]

### Fixed
- Project structure aligned for incremental sprint-based development.[cite:12]
- Repository prepared for semantic versioning from the first release.[cite:12]