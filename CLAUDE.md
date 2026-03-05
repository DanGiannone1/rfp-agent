# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development

Local dev runs natively — no Docker. Docker/container testing happens in Azure DevOps.

```bash
uv run dev.py             # starts all 3 services with hot-reload
```

This runs:
- **Session container** on :8080 (`session-container/` — `uv run uvicorn server:app`)
- **Orchestrator** on :8000 (root — `uv run uvicorn app:app`)
- **Frontend** on :3000 (`frontend/` — `npm run dev`)

### Prerequisites
- Python 3.12+ with `uv` (both root and `session-container/` have separate `pyproject.toml` + `uv.lock`)
- Node 18+ with `npm` (frontend)
- `.env` file at root (see `.env.example`). Required: `AZURE_ENDPOINT`, `AZURE_DEPLOYMENT`, `ADLS_ACCOUNT_NAME`, `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY`

### Testing (Playwright)
```bash
npx playwright test                                    # full suite (19 tests, 6 journeys)
npx playwright test -g "Journey 1"                     # chat conversation
npx playwright test -g "Journey 3: Document Conversion" # CU/ADLS pipeline
npx playwright test -g "Journey 5"                     # security & error handling
```
Tests default to `localhost:8000`/`localhost:3000`. Override with `API_URL`/`APP_URL` env vars for CI. Content Understanding and ADLS are required infrastructure — tests will fail if these services are unavailable. No skip logic.

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
    ↓ SSE stream proxy (POST /chat/stream)
Session Container (FastAPI + Copilot SDK)
    ↓ github-copilot-sdk
Azure OpenAI
```

**Key design:** The orchestrator never runs the Copilot SDK directly. It streams SSE from the session container's `/chat/stream` endpoint and passes events through to the frontend. In production, each user gets an isolated container via ACA Dynamic Sessions. Locally, a single session container serves all sessions. Sessions are tracked in-memory only (no persistence layer).

### SSE event flow
Session container streams events (delta, tool_start, tool_end, message, done, error) via `/chat/stream` → orchestrator proxies the SSE stream through to the frontend → `Chat.tsx` reducer dispatches actions per event type.

### Document processing
Uploaded files are sent directly to the session container's `/upload` endpoint and saved to the workspace. The agent uses the `convert_document` MCP tool (in `session-container/tools/convert_document.py`) to convert documents to markdown via Azure Content Understanding. ADLS is used for storage when `ADLS_ACCOUNT_NAME` is set.

### Knowledge base (optional)
Foundry IQ (Azure AI Search agentic retrieval) indexes the ADLS container and exposes a `knowledge_base_retrieve` tool to the agent via MCP. This lets the agent search across all uploaded documents, past proposals, and reference materials.

- **Setup:** Create an Azure AI Search resource (Basic tier), then run `uv run python setup_knowledge_base.py` to create the knowledge source + knowledge base. Run `uv run python index_knowledge_base.py` to upload sample data PDFs to ADLS. The indexer auto-processes documents from ADLS.
- **Agent integration:** The session container connects to the Foundry IQ MCP endpoint when `AZURE_SEARCH_ENDPOINT` is set. The Copilot SDK exposes `knowledge_base_retrieve` as a tool automatically — no custom tool code.
- **Env vars:** `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY`, `AZURE_SEARCH_KB_NAME` (default: `rfp-knowledge`). Set these in both root `.env` (for the setup script) and the session container environment (for the agent).
- **Roles:** The search service's managed identity needs `Storage Blob Data Reader` on ADLS and `Cognitive Services User` on the Foundry resource. The app's managed identity needs `Search Index Data Reader` + `Search Service Contributor` on the search service.

## Key files

- `app.py` — orchestrator endpoints (session CRUD, message streaming, file upload)
- `session_manager.py` — thin SSE proxy to session containers, manages session set, handles auth token forwarding
- `session-container/server.py` — container endpoints (/chat, /chat/stream, /status, /upload, /health)
- `session-container/agent.py` — `AgentSession` wrapping Copilot SDK with event queue, system prompt, skill_directories config
- `session-container/skills/` — 10 markdown skill files (bid-no-bid, requirements, strategy, drafting, exec summary, compliance, risk/gap, pricing analysis, customer intelligence, iterative refinement)
- `setup_knowledge_base.py` — one-time script to create Foundry IQ knowledge source + knowledge base
- `index_knowledge_base.py` — uploads sample_data PDFs to ADLS for indexing
- `mcp.json` — reference MCP server configuration (documents the Foundry IQ connection; not loaded by code — agent.py builds the config programmatically)
- `frontend/src/components/Chat.tsx` — main state machine (useReducer), session lifecycle, SSE handling
- `frontend/src/lib/sse.ts` — SSE stream parser
- `frontend/src/lib/api.ts` — backend HTTP client
- `infra/deploy.sh` — full Azure deployment (ACA, ACR, Entra ID, CosmosDB)

## Conventions

- Python: async everywhere (FastAPI + httpx + azure SDK async clients)
- Frontend: React 19, Tailwind CSS 4, TypeScript strict, `data-testid` attributes for Playwright selectors
- Two separate `uv` projects: root (orchestrator) and `session-container/` — each has its own `pyproject.toml` and `uv.lock`
- `WORKSPACE` env var controls where uploaded files land; `dev.py` sets it to an absolute path
- Docker Compose + Dockerfiles exist for CI/Azure DevOps — not used for local dev
