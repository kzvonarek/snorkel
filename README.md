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
cp MiroFish/.env.example .env
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

If you want agent memory, run only the Redis/AMS services from the `MiroFish/` Docker Compose file. Use `--scale` to avoid starting the upstream MiroFish app container:

```bash
cd MiroFish
docker compose up -d redis memory-api memory-worker
```

This starts:
- **Redis** on port `6379`
- **AMS API** on port `8000`
- **AMS task worker** (background job processor)

> **Note:** `docker compose up -d` (without specifying services) will also start the upstream `mirofish` container — that's the original MiroFish app, not this project. Only bring up the three services above.

To stop: `docker compose down`

### 2. Start the Backend

```bash
cd backend
pip install -r requirements.txt   # or: uv sync
python run.py
```

The backend starts on `http://localhost:5001`. You should see:
```
MiroFish Backend 启动完成
```

Health check: `curl http://localhost:5001/health`

### 3. Start the Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend starts on `http://localhost:3000` and automatically proxies API calls to the backend.

---

## Running Both with One Command

You can use a tool like [concurrently](https://github.com/open-cli-tools/concurrently) or just run them in separate terminals. There's no shared process manager set up yet.

```bash
# Terminal 1
cd backend && python run.py

# Terminal 2
cd frontend && npm run dev
```

---

## Deployment

There is no snorkel-specific Docker image yet. Deploy the backend and frontend manually.

> The `MiroFish/docker-compose.yml` also defines a `mirofish` service (the upstream MiroFish app) — ignore that for snorkel deployments. Only use the `redis`, `memory-api`, and `memory-worker` services from it if you need AMS.

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
├── MiroFish/               # upstream MiroFish engine (reference + Docker Compose)
│   ├── docker-compose.yml  # Redis + AMS + MiroFish container
│   └── .env.example        # env variable reference
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
