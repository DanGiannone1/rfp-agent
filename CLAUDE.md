# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development

Local dev runs natively — no Docker. Docker/container testing happens in Azure DevOps.

```bash
./dev.sh                  # starts all 3 services with hot-reload
```

This runs:
- **Session container** on :8080 (`session-container/` — `uv run uvicorn server:app`)
- **Orchestrator** on :8000 (root — `uv run uvicorn app:app`)
- **Frontend** on :3000 (`frontend/` — `npm run dev`)

### Prerequisites
- Python 3.12+ with `uv` (both root and `session-container/` have separate `pyproject.toml` + `uv.lock`)
- Node 18+ with `npm` (frontend)
- `.env` file at root (see `.env.example`). Minimum: `AZURE_ENDPOINT` and `AZURE_DEPLOYMENT`

### Testing (Playwright)
```bash
npx playwright test --project=api     # API integration tests
npx playwright test --project=e2e     # browser E2E tests
npx playwright test                   # both
```
Tests default to `localhost:8000`/`localhost:3000`. Override with `API_URL`/`APP_URL` env vars for CI.

### Frontend only
```bash
cd frontend && npm run dev      # dev server
cd frontend && npm run build    # production build
cd frontend && npm run lint     # eslint
```

## Architecture

Three-tier system where the orchestrator proxies to isolated session containers:

```
Frontend (Next.js 16, App Router)
    ↓ HTTP + SSE
Orchestrator (FastAPI)
    ↓ HTTP (blocking /chat + polling /status)
Session Container (FastAPI + Copilot SDK)
    ↓ github-copilot-sdk
Azure OpenAI
```

**Key design:** The orchestrator never runs the Copilot SDK directly. It POSTs to `/chat` on the session container (which blocks until the agent turn completes), polls `/status` for progress, and streams SSE events back to the frontend. In production, each user gets an isolated container via ACA Dynamic Sessions. Locally, a single session container serves all sessions.

### SSE event flow
Session container emits events (delta, tool_start, tool_end, message, done, error) → orchestrator re-emits status + final message as SSE → frontend `Chat.tsx` reducer dispatches actions per event type.

### Auth (optional)
Entra ID via MSAL on frontend, Easy Auth on orchestrator. Disabled locally when `NEXT_PUBLIC_ENTRA_*` vars are unset. The session manager auto-detects local vs prod: skips Azure auth tokens when `POOL_MANAGEMENT_ENDPOINT` is `http://` (not `https://`).

### Persistence (optional)
CosmosDB stores session metadata + message history. App runs fine without it (`COSMOS_ENDPOINT` unset) — sessions are in-memory only.

## Key files

- `app.py` — orchestrator endpoints (session CRUD, message streaming, file upload)
- `session_manager.py` — proxies to session containers, manages SSE polling loop, handles auth token forwarding
- `session-container/server.py` — container endpoints (/chat, /status, /upload, /health)
- `session-container/agent.py` — `AgentSession` wrapping Copilot SDK with event queue
- `cosmos.py` — async CosmosDB client (sessions + messages)
- `frontend/src/components/Chat.tsx` — main state machine (useReducer), session lifecycle, SSE handling
- `frontend/src/lib/sse.ts` — SSE stream parser
- `frontend/src/lib/api.ts` — backend HTTP client
- `infra/deploy.sh` — full Azure deployment (ACA, ACR, Entra ID, CosmosDB)

## Conventions

- Python: async everywhere (FastAPI + httpx + azure SDK async clients)
- Frontend: React 19, Tailwind CSS 4, TypeScript strict, `data-testid` attributes for Playwright selectors
- Two separate `uv` projects: root (orchestrator) and `session-container/` — each has its own `pyproject.toml` and `uv.lock`
- `WORKSPACE` env var controls where uploaded files land; `dev.sh` sets it to an absolute path
- Docker Compose + Dockerfiles exist for CI/Azure DevOps — not used for local dev
