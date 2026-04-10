---
name: bid-no-bid-analysis
description: Score an RFP opportunity across six dimensions and recommend go/no-go; use when asked whether to bid.
---

# Bid/No-Bid Analysis

## Purpose

Evaluate whether Meridian & Associates LLP should pursue an RFP opportunity by scoring it across multiple strategic dimensions. Produces a structured scorecard with a clear Go/No-Go/Conditional Go recommendation.

## When to Use

- User uploads or references a new RFP and asks whether to bid
- User asks for a "bid/no-bid", "go/no-go", or "pursuit decision"
- Early-stage opportunity assessment before committing resources
- When comparing multiple opportunities to prioritize

## Step-by-Step Process

### 1. Gather RFP Context

Read the uploaded RFP document(s) end-to-end with `read_full_file`. If the uploaded RFP is the only visible file in the workspace, call `read_full_file` without a path and start the analysis directly. Identify:
- Issuing organization and industry
- Scope of work and service lines requested
- Contract value (if stated) and duration
- Submission deadline and page/format constraints
- Evaluation criteria and weightings
- Required qualifications, certifications, or clearances
- Incumbent information (if available)

### 2. Search Knowledge Base for Precedent

Use `knowledge_base_retrieve` to find:
- Past proposals for the same client or similar engagements
- Win/loss history in this service area
- Relevant personnel qualifications and availability
- Existing client relationships or subcontractor partnerships

### 3. Score Each Dimension (1-5 Scale)

Rate the opportunity on six dimensions. For each, provide a numeric score and a brief justification:

| Dimension | What to Assess |
|---|---|
| **Strategic Fit** | Alignment with firm's practice areas (audit, tax, advisory/consulting), geographic presence, target industries, and growth strategy |
| **Capability Match** | Do we have the technical expertise, certifications, and methodologies required? Any gaps? |
| **Resource Availability** | Can we staff this engagement with qualified personnel within the timeline? Conflicts with existing commitments? |
| **Win Probability** | Competitive landscape, incumbent advantage, evaluation criteria alignment, relationship strength |
| **Past Performance** | Relevant case studies, references, and track record in similar engagements |
| **Profitability** | Expected margin given scope, pricing constraints, travel, subcontractor costs, and investment required to bid |

**Scoring Guide:**
- 5 = Excellent / Strong advantage
- 4 = Good / Above average position
- 3 = Adequate / Neutral position
- 2 = Weak / Below average position
- 1 = Poor / Significant disadvantage

### 4. Calculate Overall Score and Recommendation

- **Weighted average** (equal weights unless user specifies otherwise)
- **Recommendation thresholds:**
  - 4.0+ = **Go** — Strong pursuit candidate
  - 3.0-3.9 = **Conditional Go** — Pursue with mitigations
  - Below 3.0 = **No-Go** — Decline or monitor

### 5. Identify Key Risks and Conditions

- List the top 3-5 risks that could affect success
- For Conditional Go: specify what conditions must be met (e.g., teaming partner secured, pricing flexibility confirmed, key personnel available)

## Output Format

```markdown
## Bid/No-Bid Scorecard

**RFP:** [RFP Title / Number]
[Optional metadata lines only when known from the RFP or KB, for example:]
**Issuing Organization:** [Name]
**Due Date:** [Date]
**Estimated Value:** [Value]

### Scoring Summary

| Dimension | Score (1-5) | Rationale |
|---|:---:|---|
| Strategic Fit | X | [Brief justification] |
| Capability Match | X | [Brief justification] |
| Resource Availability | X | [Brief justification] |
| Win Probability | X | [Brief justification] |
| Past Performance | X | [Brief justification] |
| Profitability | X | [Brief justification] |
| **Overall** | **X.X** | |

### Recommendation: [Go / No-Go / Conditional Go]

[1-2 sentence summary of the recommendation rationale]

### Key Risks
1. [Risk description]
2. [Risk description]
3. [Risk description]

### Conditions for Pursuit (if Conditional Go)
- [Condition 1]
- [Condition 2]

### Next Steps
- [Action items if Go/Conditional Go, or suggested alternative if No-Go]
```

Do not use placeholder values such as "Not specified", "Unknown", or "TBD". Omit unknown fields entirely.

### 6. Save Output

Save the scorecard to the working directory as `bid_no_bid_scorecard.md` so the user can download it and it appears in the artifacts panel.

## Tools to Use

- **read_full_file**: Read the uploaded RFP and any standard analysis artifacts end-to-end
- **knowledge_base_retrieve**: Search past proposals and firm capability documents for precedent
