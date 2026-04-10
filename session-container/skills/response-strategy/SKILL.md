---
name: response-strategy
description: Develop win themes, competitive positioning, and pricing approach; use when asked for response strategy or win themes.
---

# Response Strategy Development

## Purpose

Define the strategic foundation for a winning proposal: win themes, competitive positioning, customer insights, and pricing strategy approach. Produces a strategy brief that guides all subsequent drafting.

## When to Use

- After requirements extraction, before drafting begins
- User asks for "win strategy", "response strategy", "win themes", or "competitive positioning"
- When the team needs alignment on how to approach the response
- When evaluating how to differentiate Meridian & Associates LLP from competitors

## Step-by-Step Process

### 1. Analyze the Customer

Read the RFP and use `knowledge_base_retrieve` to understand:
- **Customer organization**: Mission, structure, priorities, recent initiatives
- **Pain points**: What problems prompted this RFP? What has gone wrong before?
- **Decision drivers**: What do the evaluation criteria reveal about their true priorities?
- **Relationship history**: Has Meridian worked with this client before? In what capacity?
- **Budget signals**: Are there indications of budget constraints or willingness to invest?

If KB evidence is unavailable, rely on the RFP and cautious inference only:
- Omit customer identity, relationship history, or incumbent details unless stated in the RFP or verified through KB.
- Use phrasing like "the RFP suggests" for inferred customer priorities.
- Do not invent external proof points, named competitors, or past Meridian work.

### 2. Map the Competitive Landscape

Assess likely competitors based on:
- Incumbent (named or implied in the RFP)
- Firms with known presence in this client's industry/sector
- Requirements that seem tailored to a specific competitor
- Meridian's relative strengths and weaknesses versus likely competitors

When specific competitors are unknown, describe competitor archetypes or pressures only as inference. Do not present unnamed assumptions as verified facts.

### 3. Develop Win Themes (3-5)

Each win theme should be:
- **Client-centric**: Framed in terms of value to the customer, not Meridian's features
- **Differentiating**: Something competitors cannot easily claim
- **Provable**: Supported by evidence (past performance, case studies, metrics)
- **Relevant**: Directly tied to evaluation criteria or stated customer priorities

If external evidence is unavailable, use the RFP itself as the basis and avoid claims such as "industry references available", "prior engagements", or "sample contracts" unless they were actually retrieved.

**Common theme categories for Meridian & Associates LLP:**
- Deep industry expertise (audit, tax, advisory/consulting experience in client's sector)
- Proven methodology and quality assurance
- Team stability and senior-level engagement
- Technology-enabled service delivery
- Local presence with national/global reach
- Track record of measurable client outcomes

### 4. Define Competitive Positioning

Articulate Meridian's position using a "ghost" strategy:
- **Strengths to emphasize**: Where Meridian clearly excels
- **Competitor vulnerabilities**: Weaknesses to subtly highlight (without naming competitors)
- **Neutralizers**: How to address areas where Meridian is perceived as weaker
- **Discriminators**: Unique capabilities that only Meridian can offer

### 5. Outline Pricing Strategy Approach

Note: This is strategic guidance, not actual pricing. Consider:
- Pricing model alignment (fixed fee, hourly, blended rates, value-based)
- Investment pricing vs. market rate vs. premium positioning
- Phased approach opportunities
- Added-value inclusions only when they are grounded in the RFP or verified evidence; otherwise omit them
- Price-to-win considerations based on competitive landscape

### 6. Develop Key Messages

For each evaluator audience (technical, management, procurement), define:
- What they care about most
- Key message to deliver
- Evidence to support it

## Output Format

```markdown
## Response Strategy Brief

**RFP:** [Title / Number]
[Optional metadata lines only when known from the RFP or KB, for example:]
**Submission Date:** [Date]
**Estimated Value:** [Value]

### Customer Insights

**Organization Profile:** [Brief description grounded in the RFP; use cautious inference when needed]
**Key Pain Points:**
1. [Pain point and evidence from RFP]
2. [Pain point]
3. [Pain point]

**Decision Drivers:** [What evaluation criteria and RFP language reveal about priorities]

[Include Relationship Status only when verified]

### Win Themes

| # | Win Theme | Customer Benefit | Basis |
|---|---|---|---|
| 1 | [Theme statement] | [Value to client] | [RFP requirement or verified KB source] |
| 2 | [Theme statement] | [Value to client] | [Basis] |
| 3 | [Theme statement] | [Value to client] | [Basis] |
| 4 | [Theme statement] | [Value to client] | [Basis] |

### Competitive Positioning

[Optional: Likely Competitor Profile (if inferred, label it as inference)]

| Strategy | Details |
|---|---|
| **Strengths to Emphasize** | [List] |
| **Competitor Vulnerabilities** | [List — never name competitors in the proposal] |
| **Neutralizers** | [How to address perceived weaknesses] |
| **Discriminators** | [Unique to Meridian] |

### Pricing Strategy Approach

- **Recommended Model:** [Fixed fee / hourly / blended / etc.]
- **Positioning:** [Investment / competitive / premium]
- **Value-Add Inclusions:** [Include only when grounded in the RFP or verified evidence; otherwise omit this line]
- **Key Considerations:** [Risks, constraints, flexibility needed]

### Key Messages by Audience

| Audience | Primary Message | Basis |
|---|---|---|
| Technical Evaluators | [Message] | [RFP requirement or verified KB source] |
| Management / Executives | [Message] | [Basis] |
| Procurement / Contracts | [Message] | [Basis] |

### Response Approach

- **Proposal Structure:** [Recommended outline aligned with evaluation criteria]
- **Tone:** [Consultative / authoritative / partnership-oriented]
- **Critical Success Factors:** [What must go right to win]
```

Do not use bracketed placeholders. Omit unknown fields entirely.

### 7. Save Output

Save the strategy brief to the working directory as `response_strategy.md` so the user can download it and it appears in the artifacts panel.

After saving, reply with one short completion sentence that explicitly says the response strategy brief is ready and that it includes win themes, competitive positioning, and pricing approach. If the user said not to ask follow-up questions, do not add any invitation for more changes.

## Tools to Use

- **read_full_file**: Read the RFP, amendments, and any existing strategy artifacts end-to-end
- **knowledge_base_retrieve**: Search for past proposals to similar clients, case studies, win/loss data, competitive intelligence, approved differentiators, and relationship history — search before developing win themes or competitive positioning
