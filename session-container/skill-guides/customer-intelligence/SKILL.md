---
name: customer-intelligence
description: Create a client briefing from the RFP and knowledge base; use when asked for customer intelligence or client profile.
---

# Customer Intelligence Briefing

## Purpose

Aggregate everything known about a prospective or existing client into a structured briefing document. Synthesizes knowledge base data, RFP context, and engagement history to help pursuit teams personalize their approach and identify relationship-building opportunities.

## When to Use

- User asks for a "customer briefing", "client profile", "customer intelligence", or "client background"
- Before developing response strategy (provides inputs for win themes and positioning)
- When preparing for a client meeting or oral presentation
- When evaluating an RFP from a client Meridian has worked with before

## Step-by-Step Process

### 1. Identify the Client

Read the RFP or user input to establish:
- Organization name and any parent/subsidiary structure
- Industry and sector
- Geographic footprint
- Approximate size (revenue, employees, budget if public)

### 2. Search Knowledge Base Extensively

Run multiple `knowledge_base_retrieve` queries to surface all available information:
- "[Client name]" — direct name search
- "[Client name] engagement" — past work
- "[Client name] proposal" — past proposals submitted
- "[Industry] client" — similar clients for comparison
- "[Client name] relationship" — relationship notes
- "case study [client industry]" — relevant case studies

Also search for:
- Personnel who have worked with this client
- Service lines previously engaged
- Any quality or satisfaction data

### 3. Analyze the RFP for Client Signals

Extract implicit intelligence from the RFP itself:
- **Pain points**: What problems does the RFP language suggest?
- **Priorities**: What do evaluation criteria weightings reveal?
- **Maturity level**: How sophisticated is their understanding of the service area?
- **Budget signals**: Fixed fee vs. hourly, price weight in evaluation, budget range if stated
- **Urgency indicators**: Timeline, transition requirements, current-state problems
- **Incumbent dissatisfaction**: Language suggesting desire for change

### 4. Build Relationship Timeline

If Meridian has prior history with this client, construct a timeline:
- Past engagements (scope, dates, team, outcomes)
- Proposals submitted (won/lost, feedback received)
- Key contacts and relationship owners at Meridian
- Any known decision-makers or influencers on the client side

### 5. Assess Strategic Importance

Evaluate the client's value to Meridian:
- Revenue potential (this engagement + follow-on work)
- Reference value (brand name, industry leadership)
- Strategic fit (aligns with growth areas)
- Cross-sell opportunities (other service lines Meridian could offer)
- Competitive dynamics (who else serves this client?)

### 6. Develop Personalization Recommendations

Based on all gathered intelligence, recommend:
- How to tailor proposal language and examples to resonate with this client
- Which case studies and references are most relevant
- Which Meridian personnel to highlight (past relationship, industry expertise)
- Specific pain points to address and how to frame Meridian's solution
- Terminology and tone adjustments (match the client's style)

## Output Format

```markdown
## Customer Intelligence Briefing

**Client:** [Organization Name]
**Industry:** [Industry / Sector]
**Prepared For:** [RFP Title / Number or General Reference]
**Date:** [Date]

### Organization Profile

**Overview:** [2-3 sentence description of the organization]
**Size:** [Revenue / employees / budget if known]
**Geographic Presence:** [Locations]
**Key Business Drivers:** [What matters to this organization]

### Relationship History with Meridian

| Date | Engagement | Service Line | Team | Outcome |
|---|---|---|---|---|
| [Year] | [Engagement name] | [Audit/Tax/Advisory] | [Key personnel] | [Result / status] |
| [Year] | [Proposal submitted] | [Service line] | [Bid team] | [Won / Lost / No decision] |

**Relationship Owner:** [Partner name if known]
**Key Contacts at Client:** [Known contacts and roles]
**Relationship Health:** [Strong / Developing / New / At Risk]

### Client Priorities & Pain Points

1. **[Priority/Pain Point]** — [Evidence from RFP or past interactions]
2. **[Priority/Pain Point]** — [Evidence]
3. **[Priority/Pain Point]** — [Evidence]

### Decision-Making Insights

- **Evaluation Priorities:** [What the criteria and weights suggest]
- **Decision Style:** [Committee / individual, risk-averse / innovative, price-sensitive / quality-focused]
- **Incumbent Status:** [Current provider if known, satisfaction level, switching barriers]

### Strategic Value Assessment

| Factor | Rating | Notes |
|---|:---:|---|
| Revenue Potential | High / Medium / Low | [Current + follow-on estimate] |
| Reference Value | High / Medium / Low | [Brand recognition, industry standing] |
| Strategic Fit | High / Medium / Low | [Alignment with Meridian growth areas] |
| Cross-Sell Potential | High / Medium / Low | [Other service lines applicable] |
| Competitive Risk | High / Medium / Low | [Other firms competing for this client] |

### Personalization Recommendations

**Proposal Tailoring:**
- [Specific recommendation for tone, language, or framing]
- [Case study or reference to highlight]
- [Pain point to address directly]

**Team Positioning:**
- [Personnel to feature and why]
- [Relationship connections to leverage]

**Messaging Do's and Don'ts:**
- DO: [Approach that will resonate]
- DO: [Terminology to use]
- DON'T: [Approach to avoid]
- DON'T: [Sensitive topic or misstep to avoid]

### Information Gaps

- [What we don't know but should find out]
- [Recommended actions to fill gaps before submission]
```

### 7. Save Output

Save the briefing to the working directory as `customer_intelligence.md` so the user can download it and it appears in the artifacts panel.

## Tools to Use

- **knowledge_base_retrieve**: Primary tool — search for client name, past engagements, proposals, personnel, case studies, and industry references. Run at least 5-6 varied queries for thorough coverage.
- **bash / str_replace_editor**: Read the RFP for client signals, evaluation criteria, and context clues
- **grep**: Search RFP for organization names, incumbent references, budget indicators, and priority keywords
- **glob**: Find all documents related to this client in the working directory
