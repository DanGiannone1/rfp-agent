# Competition Presentation

Place your slide deck (`.pptx`) in this directory.

## Slide 1: Business Value Proposition

### Problem

RFP responses are manual, time-consuming, error-prone, and siloed:
- Professional services firms spend **40-80 hours per response**, with senior staff manually extracting requirements, cross-referencing compliance criteria, and drafting sections from scratch
- Institutional knowledge (past proposals, pricing history, personnel qualifications) stays locked in file shares and individual expertise
- Missed requirements and inconsistent quality lead to lost bids and compliance failures
- No systematic process for bid/no-bid decisions, risk assessment, or compliance verification

### Solution

AI-powered **RFP Response Accelerator** built on the GitHub Copilot SDK with 10 structured workflow skills and knowledge base integration:
- **Bid/No-Bid Analysis** -- scorecard-driven pursuit decisions across 6 dimensions
- **Requirements Extraction** -- automated parsing into classified compliance matrices
- **Response Strategy** -- win themes, competitive positioning, pricing approach
- **Draft Generation** -- KB-grounded proposal sections with source citations
- **Executive Summary** -- synthesized 1-2 page summaries reflecting win themes
- **Compliance Review** -- systematic pre-submission quality checks with executive sign-off tracking
- **Risk & Gap Analysis** -- risk registers with severity scoring and mitigations
- **ROI & Pricing Analysis** -- cost modeling, margin analysis, sensitivity scenarios
- **Customer Intelligence** -- client briefings with relationship history and personalization guidance
- **Iterative Refinement** -- cross-section consistency, collateral generation, review tracking

### Key Metrics

- Potential to **reduce response time by 60-70%** through automated extraction, KB-grounded drafting, and structured workflows
- **Improved compliance coverage** via systematic requirement tracking and pre-submission review
- **Leverage institutional knowledge** by connecting every response to the firm's indexed repository of past proposals, approved language, and case studies

### Enterprise Applicability

Any organization that responds to RFPs at scale: professional services firms, government contractors, system integrators, consulting firms, managed service providers, and enterprises with dedicated proposal teams.

---

## Slide 2: Technical Architecture

### Architecture

Three-tier design with per-user isolation:

```
Next.js Frontend (:3000)
    | HTTP + SSE
FastAPI Orchestrator (:8000)
    | HTTP (blocking /chat + polling /status)
Copilot SDK Session Container (:8080)
    | GitHub Copilot SDK
Azure OpenAI
```

### Key Technologies

| Technology | Role |
|------------|------|
| **GitHub Copilot SDK** | Agent framework -- manages sessions, tool execution, streaming events |
| **MCP (Model Context Protocol)** | Connects agent to Foundry IQ knowledge base |
| **Azure AI Search (Foundry IQ)** | Agentic retrieval over indexed organizational documents |
| **Azure Content Understanding** | Converts uploaded PDFs, Office docs, and images to structured markdown |
| **ACA Dynamic Sessions** | Per-user isolated containers in production |
| **Copilot SDK Skill Directories** | 7 markdown skill files loaded as agent reference material |

### Demo Highlights

1. **Upload an RFP** -- PDF is converted to markdown via Content Understanding and placed in the agent's workspace
2. **Structured analysis** -- Agent runs bid/no-bid scoring, extracts requirements into a compliance matrix, identifies risks
3. **KB-grounded drafting** -- Agent searches past proposals and approved language to generate proposal sections with citations
4. **Compliance review** -- Systematic pre-submission check produces a pass/fail checklist

### Unique Differentiators

- **Skill-driven workflows** -- 7 markdown skill files provide structured, repeatable processes with scoring frameworks and output templates, not ad-hoc prompting
- **Knowledge base grounding** -- Foundry IQ indexes real organizational data (past proposals, certifications, case studies) to reduce hallucination and ground every claim
- **Enterprise-grade isolation** -- ACA Dynamic Sessions give each user their own container with an isolated filesystem
- **Production-ready Azure deployment** -- Single-script deployment (`infra/deploy.sh`) provisions all Azure resources including Entra ID authentication, CosmosDB persistence, and ADLS document storage
- **Fully optional dependencies** -- Auth, persistence, ADLS, Content Understanding, and knowledge base are all independently optional; the app runs end-to-end with just an Azure OpenAI endpoint
