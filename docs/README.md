# RFP Agent Documentation

## Problem

Responding to Requests for Proposal is a time-consuming, manual process. Teams spend hours reading lengthy documents, extracting requirements, cross-referencing compliance criteria, and drafting responses. Key details get missed, deadlines slip, and institutional knowledge stays siloed.

## Solution

RFP Agent automates the analysis phase. Users upload RFP documents and chat with an AI agent that:

- Reads and indexes all uploaded files
- Summarizes scope, requirements, evaluation criteria, and deadlines
- Highlights compliance requirements and flags risks
- Suggests response strategies and drafts sections on request

Uploaded documents are optionally stored in ADLS Gen2 and converted to structured markdown via Azure Content Understanding, giving the agent a clean text representation alongside the original file.

The agent uses the GitHub Copilot SDK with Azure OpenAI, running in an isolated per-user container with access to shell tools (`bash`, `grep`, `glob`, `str_replace_editor`) for deep document analysis.

## Prerequisites

- **Python 3.12+** with [`uv`](https://docs.astral.sh/uv/)
- **Node 18+** with `npm`
- **Azure OpenAI** endpoint and deployment (see `.env.example`)

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd rfp-agent
   ```

2. Copy and configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env — minimum required:
   #   AZURE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/openai/v1/
   #   AZURE_DEPLOYMENT=your-deployment-name
   ```

3. Install dependencies:
   ```bash
   # Orchestrator (root)
   uv sync

   # Session container
   cd session-container && uv sync && cd ..

   # Frontend
   cd frontend && npm install && cd ..
   ```

4. Start all services:
   ```bash
   uv run dev.py
   ```
   This launches:
   | Service | Port | Directory |
   |---------|------|-----------|
   | Session Container | :8080 | `session-container/` |
   | Orchestrator | :8000 | root |
   | Frontend | :3000 | `frontend/` |

5. Open http://localhost:3000 in your browser.

### Testing

```bash
npx playwright test                           # full comprehensive suite (35 tests)
npx playwright test -g "Session Lifecycle"    # run a single test block
npx playwright test -g "SSE"                  # run by keyword
```

## Deployment

The [`infra/deploy.sh`](../infra/deploy.sh) script performs a full Azure deployment with a single command:

```bash
AZURE_ENDPOINT=https://... ./infra/deploy.sh
```

### Azure resources created

| Resource | Purpose |
|----------|---------|
| Resource Group | Contains all resources |
| User-Assigned Managed Identity | Authentication between services |
| Azure Container Registry | Hosts container images |
| Container Apps Environment | Runtime environment |
| Session Pool (Custom Container) | Isolated per-user agent sessions |
| Orchestrator Container App | API gateway, session lifecycle, SSE streaming |
| Frontend Container App | Next.js web UI |
| Entra ID App Registration | Single app reg for Easy Auth + MSAL SPA |

Optional: Set `COSMOS_ENDPOINT` for persistent session/message storage via CosmosDB. Set `ADLS_ACCOUNT_NAME` (and optionally `ADLS_FILESYSTEM`) for ADLS Gen2 document storage and Content Understanding markdown conversion.

### Configuration

Override defaults via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PREFIX` | `rfpagent` | Naming prefix for all resources |
| `LOCATION` | `eastus2` | Azure region |
| `AZURE_DEPLOYMENT` | `gpt-5-codex` | Azure OpenAI model deployment |
| `ADLS_ACCOUNT_NAME` | _(unset)_ | ADLS Gen2 storage account for document persistence |
| `ADLS_FILESYSTEM` | `documents` | ADLS filesystem (container) name |

## Architecture

```
+-------------------+
|    Frontend       |
|  (Next.js, :3000) |
+--------+----------+
         | HTTP + SSE
+--------v----------+       +-------------------------+
|   Orchestrator    |------>| ADLS Gen2               |
| (FastAPI, :8000)  |       | (document storage)      |
+--------+----------+       +-------------------------+
         |                  +-------------------------+
         |           ------>| Content Understanding   |
         |                  | (markdown conversion)   |
         |                  +-------------------------+
         | HTTP (blocking /chat + polling /status)
+--------v----------+
| Session Container |
| (FastAPI + Copilot|
|  SDK, :8080)      |
+--------+----------+
         | github-copilot-sdk
+--------v----------+
|   Azure OpenAI    |
+-------------------+
```

### Data flow

**Chat:**
1. User sends a message via the frontend
2. Frontend POSTs to the orchestrator's `/sessions/{id}/messages` endpoint
3. Orchestrator forwards the prompt to the session container's `/chat` endpoint (blocking HTTP call)
4. While `/chat` is processing, orchestrator polls `/status` on the session container
5. Status updates (thinking, tool:bash, tool:grep, etc.) are streamed as SSE events to the frontend
6. When `/chat` completes, the final message is streamed as an SSE event
7. Frontend renders the response with real-time tool activity indicators

**File upload (when ADLS/Content Understanding enabled):**
1. User uploads a file via the frontend
2. Orchestrator proxies the file to the session container's `/upload` endpoint
3. In the background, orchestrator uploads the original to ADLS Gen2 (`originals/{session_id}/`)
4. Content Understanding converts the document to markdown using `prebuilt-layout`
5. The markdown is uploaded to ADLS (`markdown/{session_id}/`) and forwarded to the session container
6. The agent can now reference both the original file and its markdown conversion

### Key design decisions

- **Orchestrator never runs the Copilot SDK** — it only proxies HTTP to session containers. This keeps the orchestrator stateless and allows per-user isolation via ACA Dynamic Sessions in production.
- **SSE is one-way** (backend to frontend). The frontend uses standard HTTP POST to send messages.
- **Auth is optional** — the app runs fully functional without Entra ID configuration, making local development frictionless.
- **Persistence is optional** — CosmosDB stores session history but the app works without it (in-memory only).
- **Content processing is optional** — when `ADLS_ACCOUNT_NAME` is set, uploaded documents are stored in ADLS Gen2 and converted to markdown via Azure Content Understanding (using the same Foundry resource as `AZURE_ENDPOINT`). The markdown is forwarded to the session container alongside the original file.

## Agent Skills

The agent loads 7 structured RFP workflow skills from markdown files in `session-container/skills/` via the Copilot SDK's `skill_directories` configuration. Each skill provides a detailed step-by-step process, scoring frameworks, and output templates that guide the agent through a specific RFP task.

| Skill | Trigger | Output Format |
|-------|---------|---------------|
| Bid/No-Bid Analysis | "Should we bid?", "go/no-go", "pursuit decision" | Scorecard (6 dimensions) with Go/No-Go/Conditional Go |
| Requirements Extraction | "Extract requirements", "compliance matrix", "parse the RFP" | Classified requirements list + compliance matrix |
| Response Strategy | "Win strategy", "win themes", "competitive positioning" | Strategy brief with themes, competitive analysis, pricing approach |
| Draft Generation | "Draft section", "write the technical approach" | Submission-ready prose with KB citations |
| Executive Summary | "Executive summary" (after other sections drafted) | 1-2 page summary: problem, solution, differentiators |
| Compliance Review | "Compliance review", "quality check", "final review" | Pass/fail checklist (requirements, instructions, terminology, tone) |
| Risk & Gap Analysis | "Risk analysis", "gap analysis", "risk register" | Risk register with severity/likelihood scores and mitigations |

Skills are plain markdown files loaded at session creation time. The Copilot SDK makes them available to the agent as reference material that informs its behavior and output structure for each workflow.

## Knowledge Base

The agent integrates with **Foundry IQ** (Azure AI Search agentic retrieval) to search Meridian & Associates LLP's indexed document repository via the `knowledge_base_retrieve` MCP tool.

### What is in the knowledge base

- **Past proposals and engagement letters** -- previously submitted RFP responses with technical approaches, staffing plans, and pricing narratives
- **Boilerplate and approved language** -- firm overview, methodology descriptions, service line capabilities
- **Personnel records and bios** -- partner, manager, and staff qualifications and certifications (CPA, CISA, CIA, etc.)
- **Case studies and past performance** -- client engagement narratives with measurable outcomes
- **Compliance and regulatory documents** -- quality control policies, peer review results, independence procedures
- **Pricing frameworks** -- rate structures, fee estimation templates, historical pricing
- **Certifications and accreditations** -- firm registrations, insurance certificates, minority/diversity certifications
- **Branding and style guidelines** -- approved descriptions, logo usage, editorial standards

### Setup

1. Ensure documents are uploaded to ADLS Gen2 (the knowledge base indexes from the same ADLS container used for document storage).
2. Create the knowledge source and knowledge base:
   ```bash
   uv run python setup_knowledge_base.py
   ```
3. Index documents into the knowledge base:
   ```bash
   uv run python index_knowledge_base.py
   ```
4. Set `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY`, and `AZURE_SEARCH_KB_NAME` (default: `rfp-knowledge`) in the session container environment.

The Copilot SDK exposes `knowledge_base_retrieve` as a tool automatically via MCP -- no custom tool code is needed.

## Responsible AI (RAI)

### Human-in-the-loop

The agent provides analysis, summaries, and draft suggestions. It does **not** autonomously submit proposals, sign documents, or make binding decisions. Every output requires human review before use.

### Data privacy

- All data stays within the user's Azure tenant — documents are processed by Azure OpenAI in the configured region
- When ADLS is enabled, documents are stored in the user's own storage account with path isolation per session (`originals/{session_id}/`, `markdown/{session_id}/`)
- Session containers are isolated per-user; one user cannot access another's documents
- No user data is used for model training
- No PII is extracted, stored, or transmitted beyond what the user explicitly uploads

### Transparency

- The frontend shows real-time tool activity (which tools the agent is using, what files it's reading) so users can observe the agent's reasoning process
- All agent outputs are clearly presented as AI-generated suggestions, not authoritative answers

### Structured workflows

- Skills provide structured, repeatable workflows (scoring frameworks, compliance matrices, output templates) that ensure systematic analysis rather than ad-hoc responses
- Each skill defines explicit steps and criteria, reducing the risk of overlooking requirements or producing inconsistent output

### KB grounding

- Knowledge base integration helps prevent hallucination by grounding generated content in real organizational data -- past proposals, approved language, personnel records, and verified certifications
- The agent cites KB sources in its output, making it straightforward for reviewers to verify claims against actual firm materials

### Limitations

- The agent's analysis quality depends on the underlying Azure OpenAI model
- It may miss nuanced legal or domain-specific requirements that require expert review
- The agent operates on uploaded documents and the knowledge base -- it has no access to external data sources or the internet
- KB retrieval quality depends on the completeness and currency of indexed documents
