# NetPulse — Architecture

## Phase 1 status
- FastAPI backend with liveness and DB health endpoints.
- PostgreSQL via Docker Compose.
- React + Vite frontend scaffold (created in Phase 1, wired in Phase 5).
- Monitoring worker: not yet implemented (Phase 3).

## Components
1. **Frontend (React + TypeScript + Vite)** — dashboard and inventory UI.
2. **Backend (FastAPI)** — REST API, validation, auth (Phase 6).
3. **Database (PostgreSQL)** — devices, results, incidents.
4. **Monitoring worker (separate process)** — runs scheduled checks.
5. **Checkers (ICMP / TCP / HTTP)** — pure, testable functions.
6. **Incident service** — threshold logic, deduplication.
7. **WebSocket layer** — pushes live updates to the frontend.

## Data flow (target)
Frontend → API → DB (targets).
Worker → checkers → DB (results) → incident service → DB (incidents) → WebSocket → Frontend.

## Decisions log
- **Phase 1:** Postgres from day one (no SQLite drift).
- **Phase 1:** Settings via pydantic-settings; `.env` gitignored.
- **Phase 1:** Worker is a separate process, never launched by FastAPI.