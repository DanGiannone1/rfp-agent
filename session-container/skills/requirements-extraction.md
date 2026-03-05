# Requirements Extraction & Compliance Matrix

## Purpose

Parse an RFP into discrete, actionable requirements. Classify each requirement by priority, build a compliance matrix, flag ambiguities, and map requirements to response outline sections.

## When to Use

- User asks to "extract requirements", "build a compliance matrix", or "parse the RFP"
- As a foundational step before drafting a response
- When the user needs to understand what the RFP is actually asking for
- When assessing whether Meridian & Associates LLP can comply with all requirements

## Step-by-Step Process

### 1. Read the Full RFP

Use `bash` or `str_replace_editor` to read the complete RFP document. Pay special attention to:
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

For each requirement, determine:
- **Mandatory (M)**: Must comply — uses language like "shall", "must", "required", "mandatory"
- **Preferred (P)**: Desired but not disqualifying — uses "should", "preferred", "desired", "ideally"
- **Informational (I)**: Context or background — no compliance needed

### 4. Assess Compliance Status

Use `knowledge_base_retrieve` to search for evidence of capability. Mark each requirement:
- **Comply (C)**: Meridian can fully meet this requirement
- **Partial Comply (PC)**: Can partially meet; note the gap
- **Exception (E)**: Cannot meet; will propose alternative approach
- **N/A**: Not applicable to Meridian's proposed solution
- **TBD**: Needs further investigation

### 5. Flag Ambiguities

Identify requirements that are:
- Vague or open to interpretation
- Contradictory with other requirements
- Missing key details (quantities, timelines, standards)
- Unusually restrictive (may be wired for a specific vendor)

### 6. Map to Response Outline

Suggest which response section each requirement should be addressed in, creating a traceability matrix between RFP requirements and proposal sections.

## Output Format

```markdown
## Requirements Analysis

**RFP:** [Title / Number]
**Total Requirements Extracted:** [Count]
**Mandatory:** [Count] | **Preferred:** [Count] | **Informational:** [Count]

### Compliance Summary
- Comply: [Count] ([Percentage]%)
- Partial Comply: [Count]
- Exception: [Count]
- TBD: [Count]

### Requirements Matrix

| ID | Source | Category | Requirement | Priority | Compliance | Response Section | Notes |
|---|---|---|---|:---:|:---:|---|---|
| REQ-001 | S2.1, p4 | Technical | [Requirement text] | M | C | Technical Approach | |
| REQ-002 | S2.3, p6 | Staffing | [Requirement text] | M | PC | Key Personnel | Gap: [detail] |
| REQ-003 | S3.1, p8 | Experience | [Requirement text] | P | C | Past Performance | |

### Ambiguities & Clarification Questions

1. **REQ-XXX** (Section X.X): [Description of ambiguity and suggested clarification question]
2. **REQ-XXX** (Section X.X): [Description of ambiguity]

### High-Risk Requirements

Requirements where compliance is uncertain or gaps exist:

| ID | Requirement | Risk | Suggested Mitigation |
|---|---|---|---|
| REQ-XXX | [Text] | [Risk description] | [Mitigation approach] |

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

- **bash / str_replace_editor**: Read RFP document sections thoroughly
- **grep**: Search for compliance-critical keywords ("shall", "must", "required", "mandatory", "certif")
- **glob**: Find all related RFP documents and attachments
- **knowledge_base_retrieve**: Search for evidence of firm capabilities, past performance, certifications, and personnel qualifications to assess compliance status
