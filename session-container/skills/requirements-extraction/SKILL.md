---
name: requirements-extraction
description: Extract and classify RFP requirements into a traceability matrix; use when asked to extract requirements or parse the RFP.
---

# Requirements Extraction

## Purpose

Parse an RFP into discrete, actionable requirements. Classify each by priority, build a traceability matrix, flag ambiguities, and map requirements to response outline sections.

## When to Use

- User asks to "extract requirements", "build a requirements matrix", or "parse the RFP"
- As a foundational step before drafting a response or running bid/no-bid analysis
- When the team needs to understand exactly what the RFP is asking for

## Step-by-Step Process

### 1. Read the Full RFP

Do not use search (grep) to extract requirements before you have read the full RFP. Read end-to-end first, then extract.

Use `bash` or `str_replace_editor` to read the complete RFP document end-to-end before any keyword search. Pay special attention to:
- Scope of work / statement of work sections
- Technical requirements
- Staffing and qualification requirements
- Administrative and submission requirements
- Terms and conditions
- Evaluation criteria
- Attachments, exhibits, and appendices (often contain critical requirements)

### 2. Extract Individual Requirements

Break the RFP into discrete requirement statements. For each requirement, capture:
- **ID**: Sequential identifier (REQ-001, REQ-002, etc.)
- **Source**: Section number and page in the original RFP
- **Requirement Text**: The actual requirement (quote or close paraphrase)
- **Category**: Group into logical categories:
  - Technical / Scope
  - Staffing / Personnel
  - Experience / Past Performance
  - Financial / Pricing
  - Administrative / Submission
  - Legal / Compliance
  - Reporting / Deliverables
  - Insurance / Bonding
  - Timeline / Schedule

### 3. Classify Priority

For each requirement, determine priority based on the full context (not just keyword hits):
- **Mandatory (M)**: Must comply — uses language like "shall", "must", "required", "mandatory"
- **Preferred (P)**: Desired but not disqualifying — uses "should", "preferred", "desired", "ideally"
- **Informational (I)**: Context or background — no compliance needed

### 4. Flag Ambiguities

Identify requirements that are:
- Vague or open to interpretation
- Contradictory with other requirements
- Missing key details (quantities, timelines, standards)
- Unusually restrictive (may be wired for a specific vendor)

### 5. Map to Response Outline

Suggest which response section each requirement should be addressed in, creating a traceability matrix between RFP requirements and proposal sections.

### 6. Save Output

Save the requirements matrix to the working directory as `requirements_matrix.md` so the user can download it and it appears in the artifacts panel. Downstream skills (compliance review, draft generation, response strategy) will reference this file.

## Output Format

```markdown
## Requirements Extraction

**RFP:** [Title / Number]
**Total Requirements:** [Count]
**Mandatory:** [Count] | **Preferred:** [Count] | **Informational:** [Count]

### Requirements Matrix

| ID | Section | Page | Category | Priority | Requirement |
|---|---|---|---|:---:|---|
| REQ-001 | 2.1 | 4 | Technical | M | [Requirement text] |
| REQ-002 | 2.3 | 6 | Staffing | M | [Requirement text] |
| REQ-003 | 3.1 | 8 | Experience | P | [Requirement text] |

### Ambiguities & Clarification Questions

1. **REQ-XXX** (Section X.X, p.X): [Description of ambiguity and suggested clarification question]
2. **REQ-XXX** (Section X.X, p.X): [Description of ambiguity]

### Suggested Response Outline

1. Executive Summary
2. Technical Approach
   - Maps to: REQ-001, REQ-004, ...
3. Key Personnel
   - Maps to: REQ-002, REQ-007, ...
4. Past Performance
   - Maps to: REQ-003, REQ-009, ...
[etc.]
```

## Tools to Use

- **bash / str_replace_editor**: Read the full RFP thoroughly end-to-end
- **grep**: Optional, only to confirm you did not miss requirements after manual extraction
- **glob**: Find all related RFP documents, attachments, and exhibits
