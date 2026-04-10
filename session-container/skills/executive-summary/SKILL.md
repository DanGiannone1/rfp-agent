---
name: executive-summary
description: Write a 1–2 page executive summary synthesizing analysis and win themes; use when asked for an executive summary.
---

# Executive Summary Generation

## Purpose

Synthesize all RFP analysis, strategy, and drafted content into a compelling 1-2 page executive summary that captures evaluator attention and communicates Meridian & Associates LLP's value proposition clearly and persuasively.

## When to Use

- User asks for an "executive summary" or "exec summary"
- After other sections have been drafted (this section references and synthesizes them)
- As the final synthesis step before submission
- Can also be drafted early as a "strawman" to align the team, then refined later

## Fast Path

If the workspace only contains the uploaded RFP markdown or does not yet contain prior analysis artifacts, draft the executive summary directly from the RFP.

- Read the uploaded RFP source markdown once with `read_full_file`, then draft immediately.
- If the uploaded RFP is the only visible file in the workspace, you can call `read_full_file` without a path.
- Do not stop to generate a response strategy brief, customer intelligence briefing, bid/no-bid analysis, or other prerequisite artifacts unless the user explicitly asks for them.
- Do not invoke `response-strategy`, `requirements-extraction`, or other skills as hidden prerequisites for this task.
- Derive provisional win themes from the RFP itself when no prior strategy brief exists.
- Use knowledge-base evidence when available, but do not block the draft on additional analysis work.

## Step-by-Step Process

### 1. Gather Inputs

Before writing, review only the context you actually need:
- **Uploaded RFP source file**: This is the primary input and should be read first
- **Response strategy brief**: Win themes, competitive positioning, key messages
- **Requirements matrix**: Scope summary, mandatory/preferred breakdown, key requirements
- **Drafted sections**: Pull key points from technical approach, past performance, staffing, pricing
- **Existing generated artifacts**: Only if they already exist and are directly relevant

If those artifacts do not exist yet, use the uploaded RFP as the primary source and draft a strong strawman executive summary from it.

Use `read_full_file` for the uploaded RFP source file and any existing generated markdown artifacts you truly need. Do not create or seek prerequisite artifacts first.

### 2. Search KB for Supporting Evidence

Use `knowledge_base_retrieve` to find:
- Firm overview and branding language for Meridian & Associates LLP
- Headline metrics (years in business, number of professionals, client count, industry rankings)
- Most compelling case studies or client outcomes relevant to this opportunity
- Awards, recognitions, or differentiating certifications

If KB evidence is unavailable or incomplete, continue drafting from the RFP and clearly avoid inventing unsupported Meridian-specific facts, case studies, or metrics.

### 3. Structure the Executive Summary

Follow this proven structure (adapt headings to match RFP requirements):

#### Opening — Customer Focus (1-2 paragraphs)
- Demonstrate understanding of the client's situation and challenges
- Reference specific language from the RFP to show attentiveness
- Connect the engagement to the client's broader strategic goals

#### Our Solution (2-3 paragraphs)
- Describe Meridian's proposed approach at a high level
- Emphasize how the approach directly addresses the client's stated needs
- Highlight innovative or differentiating elements of the methodology

#### Why Meridian (2-3 paragraphs)
- Weave in 3-5 win themes with supporting evidence
- Reference specific past engagements with measurable outcomes only when those outcomes are verified
- Highlight team qualifications and senior-level commitment
- Address any known client concerns proactively

#### Key Differentiators (bullet list or short table)
- 3-5 concise, provable differentiators
- Each tied to a client benefit, not just a Meridian feature

#### Closing — Call to Confidence (1 paragraph)
- Reaffirm commitment to the client's success
- Express enthusiasm for the partnership
- Reference next steps or availability for discussions

### 4. Save Output

Save the completed executive summary to the working directory as `executive_summary.md` using `write_file` so the user can download it and it appears in the artifacts panel.

### 5. Refine for Impact

- **Length**: Keep to 1-2 pages (roughly 500-800 words unless RFP specifies otherwise)
- **Tone**: Confident but not arrogant; client-focused, not self-congratulatory
- **First sentence**: Must immediately engage — avoid generic openings
- **Every paragraph**: Should answer "why should the evaluator care?"
- **Metrics**: Include quantified results or proof points only when verified through KB or other approved source material. If none are available, omit them.
- **Consistency**: Win themes and key messages must match the rest of the proposal
- **No placeholders**: Do not use illustrative or hypothetical proof points

## Output Format

```markdown
## Executive Summary

[Opening paragraph — demonstrate understanding of the client's situation, challenges, and objectives. Reference specific RFP language or client priorities.]

[Second paragraph — introduce Meridian's proposed approach and how it directly addresses the client's needs.]

### Our Approach

[High-level description of methodology, phasing, and key activities. Emphasize what makes the approach effective and tailored to this client.]

### Why Meridian & Associates LLP

[Win theme 1 with evidence. Win theme 2 with evidence. Demonstrate relevant experience, team quality, and commitment.]

[Reference a specific past engagement only when the engagement and outcome are verified. Otherwise omit this sentence.]

### Key Differentiators

| Differentiator | Client Benefit |
|---|---|
| [Differentiator 1] | [How this helps the client] |
| [Differentiator 2] | [How this helps the client] |
| [Differentiator 3] | [How this helps the client] |

### Our Commitment

[Closing paragraph — reaffirm commitment, express enthusiasm for the partnership, and invite further dialogue.]

---

*Note: This executive summary reflects the response strategy brief when one exists; otherwise it uses win themes inferred directly from the RFP. Include only verified metrics and cite their sources when used.*
```

## Tools to Use

- **read_full_file**: Read the uploaded RFP and any existing markdown deliverables in the working directory
- **write_file**: Save the completed executive summary artifact to the working directory
- **knowledge_base_retrieve**: Search for firm overview language, headline metrics, compelling case studies, branding guidelines, and approved boilerplate
