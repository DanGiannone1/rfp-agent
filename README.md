# RFP Agent

RFP Agent is an AI-powered proposal response accelerator built on the GitHub Copilot SDK. It transforms the manual, time-intensive process of responding to Requests for Proposal into a guided, AI-assisted workflow. Users upload RFP documents and interact with a conversational agent equipped with seven structured skills — bid/no-bid analysis, requirements extraction, response strategy, draft generation, executive summary writing, compliance review, and risk/gap analysis. The agent searches a Foundry IQ knowledge base of past proposals, certifications, personnel records, and pricing frameworks via MCP to ground its responses in organizational knowledge. Built on a three-tier architecture (Next.js frontend, FastAPI orchestrator, sandboxed Copilot SDK session containers), it deploys to Azure Container Apps with per-user isolation, optional Entra ID authentication, ADLS Gen2 document storage with Content Understanding markdown conversion, and CosmosDB persistence. Designed for enterprise teams that respond to dozens of RFPs annually.

## Architecture

```
Frontend (Next.js, App Router)
    | HTTP + SSE
Orchestrator (FastAPI)
    | HTTP (blocking /chat + polling /status)
    |                          \--- ADLS Gen2 (document storage)
    |                          \--- Content Understanding (markdown conversion)
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
