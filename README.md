# Snorkel — PMF Simulation Studio

Snorkel is a Product-Market Fit analysis tool built on the [MiroFish](https://github.com/666ghj/MiroFish) swarm intelligence engine. It spins up LLM agents that take on personas derived from your customer data, simulates their reactions to a product or idea, and generates a structured PMF report you can chat with.

## Architecture

```
frontend/   Vue 3 + Vite            → http://localhost:3000
backend/    Flask (Python 3.11+)    → http://localhost:5001
```

The frontend proxies all `/api` requests to the backend (configured in `frontend/vite.config.js`). The backend optionally connects to an Agent Memory Server (AMS) backed by Redis for persistent agent memory across simulation rounds.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Node.js | 18+ |
| Python | 3.11 – 3.12 |
| pip or uv | latest |
| Docker + Docker Compose | for Redis/AMS (optional but recommended) |

---

## Environment Setup

Create a `.env` file in the **repo root** (`snorkel/.env`). The backend loads it from there automatically.

```bash
cp .env.example .env
```

Then fill in the required values:

### Required

```env
# LLM API — any OpenAI-compatible provider works (OpenAI, Alibaba Qwen, etc.)
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.openai.com/v1      # or https://dashscope.aliyuncs.com/compatible-mode/v1 for Qwen
LLM_MODEL_NAME=gpt-4o-mini                 # or qwen-plus, etc.
```

### Optional — Agent Memory Server (AMS)

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

```bash
docker compose up -d redis memory-api memory-worker
```

This starts:
- **Redis** on port `6379`
- **AMS API** on port `8000`
- **AMS task worker** (background job processor)

To stop: `docker compose down`

### 2. Install dependencies

```bash
npm run setup:all
```

This installs root npm packages, frontend npm packages, and backend Python packages.

### 3. Start both services

```bash
npm run dev
```

This runs the backend and frontend concurrently. The backend starts on `http://localhost:5001` and the frontend on `http://localhost:3000`.

Health check: `curl http://localhost:5001/health`

---

## Deployment

### Docker

Build and run the full stack with Docker Compose:

```bash
docker compose up -d
```

Or build just the Snorkel image:

```bash
docker compose build snorkel
```

### Manual Deployment

**Backend:**

```bash
cd backend
pip install -r requirements.txt
# Set environment variables (or use a .env file)
export LLM_API_KEY=...
python run.py
```

For production, run behind gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 "app:create_app()"
```

**Frontend:**

```bash
cd frontend
npm install
npm run build       # outputs to frontend/dist/
```

Serve `frontend/dist/` with any static host (nginx, Vercel, Netlify, etc.). Set the `VITE_API_BASE_URL` env var if your backend is on a different domain:

```env
VITE_API_BASE_URL=https://your-backend.example.com
```

---

## Project Structure

```
snorkel/
├── .env                    # your environment variables (create this)
├── .env.example            # environment variable template
├── package.json            # root npm scripts (dev, build, setup)
├── Dockerfile              # multi-stage build for frontend + backend
├── docker-compose.yml      # Redis + AMS + Snorkel services
├── backend/                # Flask API server
│   ├── app/
│   │   ├── api/            # route handlers (simulation, report)
│   │   ├── services/       # core logic (simulation runner, memory, personas)
│   │   ├── models/         # project/simulation data models
│   │   └── config.py       # loads .env from repo root
│   ├── requirements.txt
│   └── run.py              # entry point → http://localhost:5001
├── frontend/               # Vue 3 app
│   ├── src/
│   │   ├── api/            # axios wrappers for backend endpoints
│   │   ├── views/          # page components
│   │   └── main.js
│   ├── vite.config.js      # proxies /api → localhost:5001
│   └── package.json        # entry point → http://localhost:3000
└── planning/               # design docs and wireframes
```

---

## Key API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Backend health check |
| POST | `/api/simulation/create` | Create a new simulation |
| POST | `/api/simulation/start` | Start a simulation |
| GET | `/api/simulation/list` | List simulations |
| GET | `/api/simulation/{id}` | Get simulation status/details |
| POST | `/api/simulation/interview/batch` | Interview agents post-simulation |
| POST | `/api/report/generate` | Generate PMF report |
| GET | `/api/report/list` | List reports |
| GET | `/api/report/{id}` | Get a report |
| POST | `/api/report/chat` | Chat with a report |
| POST | `/api/graph/build` | Build agent knowledge graph |

---

## Troubleshooting

**`LLM_API_KEY 未配置` on startup** — The backend can't find your `.env`. Make sure it lives at `snorkel/.env` (repo root), not inside `backend/`.

**AMS connection errors** — If you see memory-related errors but don't need persistent memory, set `AMS_ENABLED=false` in your `.env`.

**Frontend shows blank or CORS errors** — Make sure the backend is running on port 5001 before starting the frontend. The Vite proxy handles CORS in dev; in production you'll need CORS headers on the backend or a reverse proxy.

**Python version errors** — The backend requires Python 3.11 or 3.12 (not 3.13+). Check with `python --version`.
