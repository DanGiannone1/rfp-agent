# RFP Agent

An AI-powered agent that automates the analysis of Requests for Proposal (RFPs). Users upload RFP documents and interact with a conversational agent that reads, summarizes, and helps draft responses — extracting key requirements, compliance criteria, deadlines, and risks. Built on a three-tier architecture with isolated per-user sessions: a Next.js frontend streams real-time agent activity via SSE, a FastAPI orchestrator manages session lifecycle, and sandboxed session containers run the GitHub Copilot SDK against Azure OpenAI. Deploys to Azure Container Apps with Dynamic Sessions for per-user isolation, optional Entra ID authentication, and optional CosmosDB persistence.

## Architecture

```
Frontend (Next.js, App Router)
    | HTTP + SSE
Orchestrator (FastAPI)
    | HTTP (blocking /chat + polling /status)
Session Container (FastAPI + Copilot SDK)
    | github-copilot-sdk
Azure OpenAI
```

## Quick Links

- [Full Documentation](docs/README.md) — setup, deployment, architecture details
- [Agent Specification](AGENTS.md) — agent identity, tools, and behavioral guidelines
- [CLAUDE.md](CLAUDE.md) — development conventions and commands
- [Deployment Script](infra/deploy.sh) — one-command Azure deployment
- [Presentation Outline](presentations/README.md) — slide deck structure
