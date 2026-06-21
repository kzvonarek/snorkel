# Snorkel Monorepo

This repository contains a full-stack multi-agent simulation platform with:

- A Python backend (`Flask`) for simulation orchestration and report generation.
- A Vue frontend (`Vite`) for project setup, scenario execution, and results.
- Optional memory infrastructure (`Redis` + `agent-memory-server`) for long-term state.
- Planning and product docs used during development.
- A legacy MiroFish frontend snapshot preserved outside the main app code.

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

AMS gives agents persistent long-term memory across simulation rounds using Redis. Without it the app still works but agents won't remember previous rounds.

```env
AMS_ENABLED=true
AMS_BASE_URL=http://localhost:8000          # where the memory API runs
AMS_API_KEY=                               # leave blank if DISABLE_AUTH=true
AMS_TIMEOUT=30
AMS_GENERATION_MODEL=gpt-4o-mini           # model used by AMS for memory summarization
AMS_EMBEDDING_MODEL=text-embedding-3-small # model used by AMS for vector search
```

> **Note:** AMS uses OpenAI's API for its own embedding and generation calls, independent of your `LLM_API_KEY`. Make sure the key you use has access to the models specified in `AMS_GENERATION_MODEL` and `AMS_EMBEDDING_MODEL` if you're using OpenAI.

### Optional — Third-party integrations

All three integrations are **opt-in** and fail gracefully — the app runs normally with none of them configured.

#### The Token Company (prompt compression)

Compresses LLM prompts before every agent call, reducing token usage and cost by 10–40%.

1. Get an API key at [thetokencompany.com](https://thetokencompany.com)
2. Add to `.env`:

```env
TOKEN_COMPANY_ENABLED=true
TOKEN_COMPANY_API_KEY=ttc-your-key-here
TOKEN_COMPANY_MIN_CHARS=2000    # don't compress prompts shorter than this
```

The hook sits inside `LLMClient.chat()` and runs transparently on every agent LLM call. JSON-mode calls are excluded automatically.

#### Browserbase / Stagehand (agent web browsing)

Gives the report agent three new tools — `browse_web`, `extract_web_data`, and `observe_web` — so it can fetch live web context using a real headless browser, not just simulation graph data.

1. Sign up at [browserbase.com](https://browserbase.com) and create a project.
2. Install Playwright's Chromium runtime (needed by the Stagehand client):

```bash
cd backend
playwright install chromium
```

3. Add to `.env`:

```env
BROWSERBASE_ENABLED=true
BROWSERBASE_API_KEY=your-api-key
BROWSERBASE_PROJECT_ID=your-project-id
```

The web tools only appear in the agent's tool list when `BROWSERBASE_ENABLED=true` and both credentials are present.

#### Sentry (error monitoring & performance tracing)

Auto-captures unhandled exceptions across all Flask routes and creates performance traces for:
- Every HTTP request (via `FlaskIntegration`)
- `generate_report`, `plan_outline`, `_generate_section_react`, `chat` (agent-level)
- Each individual tool call with latency tagging
- Every LLM call with model + token metadata

1. Create a project at [sentry.io](https://sentry.io) and copy your DSN.
2. Add to `.env`:

```env
SENTRY_DSN=https://your-dsn@oXXXXXX.ingest.sentry.io/XXXXXXX
SENTRY_TRACES_SAMPLE_RATE=0.2   # 20% of transactions; set to 1.0 in dev
SENTRY_ENVIRONMENT=production
```

### Optional — tuning

```env
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5001
OASIS_DEFAULT_MAX_ROUNDS=10
REPORT_AGENT_MAX_TOOL_CALLS=5
REPORT_AGENT_MAX_REFLECTION_ROUNDS=2
REPORT_AGENT_TEMPERATURE=0.5
```

---

## Running Locally

### 1. Start Redis + Agent Memory Server (optional)

If you want agent memory, start the Redis/AMS services:
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
