# Snorkel Monorepo

This repository contains a full-stack multi-agent simulation platform with:

- A Python backend (`Flask`) for simulation orchestration and report generation.
- A Vue frontend (`Vite`) for project setup, scenario execution, and results.
- Optional memory infrastructure (`Redis` + `agent-memory-server`) for long-term state.
- Planning and product docs used during development.

## Repository Layout

Top-level folders:

- `backend/`: Python API, simulation services, scripts, tests.
- `frontend/`: Current primary Vue application.
- `frontend-legacy/`: Archived alternate MiroFish frontend 
- `docs/`: Archived original MiroFish README files.
- `locales/`: Locale resources moved from MiroFish.
- `static/`: Images/screenshots/assets moved from MiroFish.
- `planning/`: Architecture and wireframe planning notes.

Key root files:

- `.env.example`: Environment variable template.
- `package.json`: Root scripts for setup and unified run.
- `Dockerfile`: Containerized full-stack app build.
- `docker-compose.yml`: Local stack for app + Redis + memory services.
- `LICENSE`: Project license file.

## Quick Start (Local)

Prerequisites:

- Node.js `>=18`
- Python `>=3.11,<3.13`
- `uv` installed for Python dependency management

1. Configure environment variables:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
npm run setup:all
```

3. Run frontend + backend together:

```bash
npm run dev
```

Default endpoints:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5001`

Run services individually:

```bash
npm run backend
npm run frontend
```

## Docker

From repo root:

```bash
cp .env.example .env
docker compose up --build
```

This starts:

- `app` on ports `3000` and `5001`
- `redis` on `6379`
- `memory-api` on `8000`
- `memory-worker` as background processing service

## Backend Notes

- Main entry: `backend/run.py`
- App bootstrap: `backend/app/__init__.py`
- API routes: `backend/app/api/`
- Core simulation services: `backend/app/services/`
- Tests: `backend/tests/`

Typical backend commands:

```bash
cd backend
uv sync
uv run python run.py
uv run pytest
```

## Frontend Notes

- Main app entry: `frontend/src/main.js`
- App shell and pages: `frontend/src/views/`
- API clients: `frontend/src/api/`
- Shared UI components: `frontend/src/components/`

Build command:

```bash
cd frontend
npm run build
```

## Migration Summary (MiroFish Consolidation)

Moved to root:

- `.env.example`
- `.dockerignore`
- `Dockerfile`
- `docker-compose.yml`
- `package.json`
- `package-lock.json`
- `LICENSE`
- `locales/`
- `static/`

Moved to archive locations:

- `MiroFish/frontend/` -> `frontend-legacy/`
- `MiroFish/README.md` -> `docs/README-MiroFish-original.md`
- `MiroFish/README-ZH.md` -> `docs/README-MiroFish-original-ZH.md`

## Additional Documentation

- Original English project readme snapshot: `docs/README-MiroFish-original.md`
- Original Chinese project readme snapshot: `docs/README-MiroFish-original-ZH.md`
- Planning docs: `planning/backend-plan.md`, `planning/pmf-app-wireframes.html`
