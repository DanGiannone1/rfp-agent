# Application Agent Runtime Spec

This document describes the runtime behavior of the shipped RFP application agent.

It is not a contributor instruction file for Codex, Claude Code, Gemini CLI, or any other coding agent working on this repository.

## Runtime Boundary

- This spec applies to the in-product RFP assistant that runs inside the session container.
- The primary runtime prompt implementation lives in [session-container/agent.py](/home/dan/projects/rfp-agent/session-container/agent.py).
- The workflow skill assets live in [session-container/skills](/home/dan/projects/rfp-agent/session-container/skills).
- Coding agents modifying this repository should follow `AGENTS.md`, not this document.

## Runtime Identity

The shipped application agent is an RFP Response Accelerator for professional services firms focused on audit, tax, and advisory or consulting engagements. Its job is to help pursuit teams analyze RFPs, develop response strategy, and generate high-quality proposal artifacts.

## Runtime Tools

The runtime agent is designed around:

- workspace file tools for reading and writing deliverables
- knowledge-base retrieval for firm-approved content and evidence
- markdown and CSV artifact generation
- document conversion to markdown for uploaded source materials

## Runtime Workflow Model

The runtime agent is expected to:

- orient on uploaded files first
- read RFP documents before searching
- follow structured skill workflows instead of improvising
- ground claims in firm materials when the knowledge base is available
- save narrative outputs as markdown and structured outputs as CSV or JSON

## Runtime Skills

The current runtime skill set includes:

1. Bid/No-Bid Analysis
2. Requirements Extraction
3. Response Strategy
4. Draft Generation
5. Executive Summary
6. Compliance Review
7. Risk and Gap Analysis
8. ROI and Pricing Analysis
9. Customer Intelligence
10. Iterative Refinement

The executable skill markdown files are in [session-container/skills](/home/dan/projects/rfp-agent/session-container/skills).

## Runtime Prompt Source of Truth

The user-facing runtime prompt is implemented in code, not here. When changing application-agent behavior, update the real source files:

- [session-container/agent.py](/home/dan/projects/rfp-agent/session-container/agent.py)
- [session-container/skills](/home/dan/projects/rfp-agent/session-container/skills)

Keep this document descriptive, not authoritative.
