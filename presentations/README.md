# Presentations

Place your slide deck (`.pptx`) in this directory.

## Suggested Outline

### Slide 1: Business Value Proposition

- **Problem**: RFP response is slow, manual, and error-prone — teams spend hours extracting requirements and drafting responses
- **Solution**: AI agent that reads, analyzes, and helps respond to RFPs through a conversational interface
- **Key value**: Reduces analysis time, catches missed requirements, maintains compliance awareness
- **Project summary** (copy-paste ready for submission form — see top of [README.md](../README.md))

### Slide 2: Architecture and Demo

- Architecture diagram (see [docs/README.md](../docs/README.md#architecture))
- Three-tier design: Frontend (Next.js) -> Orchestrator (FastAPI) -> Session Container (Copilot SDK) -> Azure OpenAI
- Per-user isolation via ACA Dynamic Sessions
- Link to repository
