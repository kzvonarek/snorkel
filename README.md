# Snorkel PMF Simulation Studio

Snorkel turns curated customer personas and a product brief into an OASIS social simulation. Product teams can watch agent activity, inspect observed results, generate a Markdown research report, and chat with the report.

The demo has two explicit modes:

- **Live OASIS** runs the Flask, LLM, and OASIS pipeline.
- **Demo data** uses deterministic fixtures if live preparation cannot start. A yellow banner always identifies fixture output; it is never presented as live evidence.

## Five-Minute Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11 or 3.12 (Python 3.13 is not supported by the OASIS dependency set)
- [uv](https://docs.astral.sh/uv/)
- An API key for an OpenAI-compatible chat-completions provider

Create the environment file:

```powershell
Copy-Item .env.example .env
```

Set at least these values in `.env`:

```env
LLM_API_KEY=your_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4o-mini
AMS_ENABLED=false
```

Install dependencies:

```powershell
npm install
npm --prefix frontend install
Set-Location backend
uv sync --dev
Set-Location ..
```

Start both applications:

```powershell
npm run dev
```

Open `http://localhost:3000`. The backend health check is `http://localhost:5001/health`.

## Demo Walkthrough

1. Open **All projects** and select **New project**.
2. Choose one of the three curated studies: Orbit Note, Emberwild, or Harbor Commons. Each includes nine personas, a topic-specific real-time thought sequence, results, and a downloadable PDF report.
3. Watch the colored agents move and generate thoughts in **Live swarm feed**.
4. Continue to **Results dashboard**, then open **Report & chat** to download the matching PDF.

For the live OASIS path:

1. Open **Configure run**.
2. Drag at least one persona segment and one product asset onto the canvas. Market context is optional.
3. Keep the run small for a presentation: 2-5 rounds and 1-2 agents per segment.
4. Select **Run simulation**. Snorkel creates the project, prepares persona profiles, and starts a Twitter-style OASIS run.

## Architecture

```text
frontend/   Vue 3 + Vite                 http://localhost:3000
backend/    Flask + OASIS + report agent http://localhost:5001
Redis AMS   optional post-run indexing   http://localhost:8000
```

OASIS owns the agents' in-round social environment and SQLite activity ledger. Redis Agent Memory Server is optional infrastructure for indexing and retrieving activity after it is emitted; it is not OASIS's native in-round memory.

The active browser run is stored in `sessionStorage`, so moving among Swarm, Results, and Report does not discard it. Live and fixture adapters expose the same normalized frontend state.

## Optional Redis AMS

For activity indexing and semantic retrieval, enable AMS in `.env` and start its services:

```powershell
docker compose up -d redis memory-api memory-worker
```

```env
AMS_ENABLED=true
AMS_BASE_URL=http://localhost:8000
AMS_API_KEY=
AMS_TIMEOUT=30
AMS_GENERATION_MODEL=gpt-4o-mini
AMS_EMBEDDING_MODEL=text-embedding-3-small
```

AMS may use separate generation and embedding models. Confirm that the supplied provider key supports both.

## Tests and Build

Use Python 3.11 or 3.12 and run backend tests from the backend directory so `app` resolves correctly:

```powershell
Set-Location backend
uv run pytest tests -q
Set-Location ..
npm --prefix frontend test
npm run build
```

## API Surface

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Backend health |
| `POST` | `/api/projects` | Persist a product brief and simulation requirement |
| `GET` | `/api/projects` | List projects |
| `GET` | `/api/projects/{id}` | Retrieve a project and its text context |
| `POST` | `/api/simulation/create` | Create a simulation for a project |
| `POST` | `/api/simulation/prepare` | Generate config and profiles from persona inputs |
| `POST` | `/api/simulation/prepare/status` | Poll preparation |
| `POST` | `/api/simulation/start` | Start an OASIS run |
| `GET` | `/api/simulation/{id}/run-status` | Poll run progress |
| `GET` | `/api/simulation/{id}/actions` | Read observed actions |
| `GET` | `/api/simulation/{id}/timeline` | Read round summaries |
| `GET` | `/api/simulation/{id}/agent-stats` | Read activity by agent |
| `POST` | `/api/report/generate` | Start Markdown report generation |
| `POST` | `/api/report/generate/status` | Poll report generation |
| `GET` | `/api/report/{id}` | Retrieve a report |
| `GET` | `/api/report/{id}/download` | Download Markdown |
| `POST` | `/api/report/chat` | Chat with the report agent |

## Project Layout

```text
backend/app/api/        Flask route handlers
backend/app/services/   OASIS runner, persona, memory, and reporting logic
backend/tests/          Backend contract and service tests
frontend/src/api/       HTTP client wrappers
frontend/src/composables/useRun.js  Persisted live/fixture orchestration
frontend/src/views/     Demo workflow screens
planning/               Product plan, wireframes, and presentation material
```

## Troubleshooting

**`ModuleNotFoundError: flask` or another Python package**

Run `uv sync --dev` inside `backend`, then use `uv run python run.py` or the root `npm run dev` command. A root `.venv` created with Python 3.13 is not compatible with this project.

**The app immediately shows Demo data**

Read the yellow banner for the live failure reason. Common causes are a missing `.env`, an invalid `LLM_API_KEY`, an unsupported model, or the backend not running on port 5001. After correcting the issue, return to Configure run and start a new run.

**AMS connection failures**

Set `AMS_ENABLED=false` for the core demo, or verify `docker compose ps` and `http://localhost:8000/health` before enabling indexing.

**Frontend build fails with an access error under OneDrive**

OneDrive or managed filesystem policies can prevent esbuild from traversing parent directories. Run the build from a normal local checkout outside a synchronized folder, or allow the Node/esbuild process access to the workspace. This is distinct from a Vue compilation error.

**The report takes a long time**

Live report generation performs multiple LLM calls. Use fewer agents and rounds for a presentation. Fixture mode produces a deterministic report immediately.

## Current Boundaries

- Inputs are curated product briefs, persona segments, and market context already represented in the demo UI.
- Curated demo studies include verified three-page PDFs. Reports generated by the live OASIS backend remain Markdown; dynamic PDF export is a later milestone.
- File uploads, CSV persona import, production connectors, evidence-linked PMF scoring, and structured sentiment analysis are subsequent milestones.
- The initial live path uses the Twitter-style OASIS environment for reliability.
