# Changelog - Koi

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- HTTPBearer integration for Swagger-friendly authentication flow.[cite:35]
- Password hashing with bcrypt or equivalent.[cite:35]
- Stronger token strategy beyond mock tokens.[cite:35]
- Masked IBAN exposure and richer balance modeling.[cite:12]
- Chat orchestration with internal banking tools.[cite:12]
### Added
- `/tests/recent` test_smoke.py
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