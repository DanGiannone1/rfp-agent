# Risk & Gap Analysis

## Purpose

Identify technical risks, compliance gaps, resource constraints, and dependencies that could affect proposal success or engagement delivery. Score each by severity and likelihood, and propose actionable mitigations. Produces a risk register for pursuit decision-making and proposal planning.

## When to Use

- User asks for a "risk analysis", "gap analysis", "risk assessment", or "risk register"
- After requirements extraction to identify compliance gaps
- As part of bid/no-bid analysis to quantify risks
- During proposal development to proactively address weaknesses
- When evaluating whether to pursue with a teaming partner or subcontractor

## Step-by-Step Process

### 1. Review All Available Inputs

Read the RFP, requirements matrix, strategy brief, and any drafted sections to identify risk sources:

Use `bash` and `glob` to find all relevant files. Key areas to examine:
- Scope of work — are there areas outside Meridian's core competencies?
- Staffing requirements — can we staff with qualified personnel?
- Timeline — is the delivery schedule realistic?
- Terms and conditions — are there onerous provisions?
- Pricing constraints — is there margin risk?
- Evaluation criteria — are we weak in heavily weighted areas?

### 2. Categorize Risks

Organize identified risks into these categories:

| Category | What to Look For |
|---|---|
| **Technical** | Scope complexity, unfamiliar methodologies, technology requirements, deliverable ambiguity |
| **Compliance** | Mandatory requirements Meridian cannot fully meet, certification gaps, regulatory requirements |
| **Resource** | Staffing availability, key personnel conflicts, skill gaps, capacity constraints |
| **Financial** | Pricing pressure, cost estimation uncertainty, scope creep potential, payment terms |
| **Schedule** | Aggressive timelines, dependencies on client actions, concurrent commitments |
| **Competitive** | Incumbent advantage, wired requirements, evaluation criteria misalignment |
| **Legal/Contractual** | Liability exposure, IP provisions, indemnification, insurance requirements, non-compete clauses |
| **Reputational** | Client relationship risk, public visibility, regulatory scrutiny |

### 3. Search KB for Historical Context

Use `knowledge_base_retrieve` to find:
- Lessons learned from similar past engagements
- Risk mitigations that worked in prior proposals
- Personnel with relevant experience to address gaps
- Teaming partners or subcontractors used previously

### 4. Score Each Risk

Use a 5x5 severity/likelihood matrix:

**Likelihood:**
- 5 = Almost Certain (>90%)
- 4 = Likely (60-90%)
- 3 = Possible (30-60%)
- 2 = Unlikely (10-30%)
- 1 = Rare (<10%)

**Severity (Impact):**
- 5 = Critical — Disqualification or engagement failure
- 4 = Major — Significant cost/schedule overrun or compliance issue
- 3 = Moderate — Manageable but requires active mitigation
- 2 = Minor — Limited impact, easily addressed
- 1 = Negligible — Minimal consequence

**Risk Score** = Likelihood x Severity
- 15-25 = **Critical** (must mitigate before proceeding)
- 8-14 = **High** (require mitigation plan)
- 4-7 = **Medium** (monitor and plan)
- 1-3 = **Low** (accept and document)

### 5. Develop Mitigations

For each medium-and-above risk, propose:
- **Mitigation strategy**: How to reduce likelihood or impact
- **Owner**: Who at Meridian should own this risk
- **Timeline**: When must the mitigation be in place
- **Cost/effort**: What resources are needed for mitigation
- **Residual risk**: Risk level after mitigation is applied

### 6. Identify Gaps Requiring Action

Separate out gaps that need immediate action:
- Missing certifications or qualifications
- Personnel gaps requiring recruitment or teaming
- Technology or methodology gaps
- Past performance gaps in required areas
- Missing information requiring RFP clarification questions

## Output Format

```markdown
## Risk & Gap Analysis

**RFP:** [Title / Number]
**Date:** [Date]
**Risk Assessment Level:** [High / Medium / Low — overall assessment]

### Risk Summary

| Risk Level | Count |
|---|:---:|
| Critical (15-25) | [N] |
| High (8-14) | [N] |
| Medium (4-7) | [N] |
| Low (1-3) | [N] |

### Risk Register

| ID | Category | Risk Description | Likelihood (1-5) | Severity (1-5) | Score | Level | Mitigation Strategy | Owner | Status |
|---|---|---|:---:|:---:|:---:|:---:|---|---|:---:|
| R-001 | Technical | [Description] | 3 | 4 | 12 | High | [Mitigation] | [Role] | Open |
| R-002 | Compliance | [Description] | 4 | 5 | 20 | Critical | [Mitigation] | [Role] | Open |
| R-003 | Resource | [Description] | 2 | 3 | 6 | Medium | [Mitigation] | [Role] | Open |

### Critical & High Risks — Detail

#### R-001: [Risk Title]
- **Description:** [Detailed description of the risk]
- **Root Cause:** [Why this risk exists]
- **Impact if Realized:** [Specific consequences]
- **Mitigation Plan:** [Step-by-step mitigation approach]
- **Residual Risk:** [Risk level after mitigation]
- **Decision Point:** [When/how to decide if risk is acceptable]

#### R-002: [Risk Title]
[Same structure]

### Gap Analysis

| Gap ID | Category | Description | Impact | Required Action | Priority | Timeline |
|---|---|---|---|---|:---:|---|
| G-001 | Staffing | [Gap description] | [Impact on proposal/delivery] | [Action needed] | High | [When] |
| G-002 | Certification | [Gap description] | [Impact] | [Action needed] | Critical | [When] |

### Recommendations

1. **Proceed / Do Not Proceed:** [Based on risk profile]
2. **Must-Address Before Submission:**
   - [Action item 1]
   - [Action item 2]
3. **Teaming/Subcontracting Needs:**
   - [Partner type needed for gap area]
4. **Clarification Questions to Submit:**
   - [Question to reduce ambiguity on risk area]
```

## Tools to Use

- **bash / glob**: Read RFP terms and conditions, scope documents, and all proposal materials
- **str_replace_editor**: Examine specific contractual clauses, requirement details, and drafted content
- **grep**: Search for risk indicators ("penalty", "liquidated damages", "termination", "liability", "warranty", "indemnif", "insurance", "bond")
- **knowledge_base_retrieve**: Search for lessons learned, past risk mitigations, teaming history, and capability evidence to assess gaps
