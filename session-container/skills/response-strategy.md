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

### 2. Map the Competitive Landscape

Assess likely competitors based on:
- Incumbent (named or implied in the RFP)
- Firms with known presence in this client's industry/sector
- Requirements that seem tailored to a specific competitor
- Meridian's relative strengths and weaknesses versus likely competitors

### 3. Develop Win Themes (3-5)

Each win theme should be:
- **Client-centric**: Framed in terms of value to the customer, not Meridian's features
- **Differentiating**: Something competitors cannot easily claim
- **Provable**: Supported by evidence (past performance, case studies, metrics)
- **Relevant**: Directly tied to evaluation criteria or stated customer priorities

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
- Added-value inclusions that differentiate without adding cost
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
**Client:** [Organization]
**Submission Date:** [Date]
**Estimated Value:** [Value]

### Customer Insights

**Organization Profile:** [Brief description]
**Key Pain Points:**
1. [Pain point and evidence from RFP]
2. [Pain point]
3. [Pain point]

**Decision Drivers:** [What evaluation criteria and RFP language reveal about priorities]

**Relationship Status:** [New client / Existing relationship / Past engagement details]

### Win Themes

| # | Win Theme | Customer Benefit | Supporting Evidence |
|---|---|---|---|
| 1 | [Theme statement] | [Value to client] | [Case study, metric, or reference] |
| 2 | [Theme statement] | [Value to client] | [Evidence] |
| 3 | [Theme statement] | [Value to client] | [Evidence] |
| 4 | [Theme statement] | [Value to client] | [Evidence] |

### Competitive Positioning

**Primary Competitors:** [Known or likely competitors]

| Strategy | Details |
|---|---|
| **Strengths to Emphasize** | [List] |
| **Competitor Vulnerabilities** | [List — never name competitors in the proposal] |
| **Neutralizers** | [How to address perceived weaknesses] |
| **Discriminators** | [Unique to Meridian] |

### Pricing Strategy Approach

- **Recommended Model:** [Fixed fee / hourly / blended / etc.]
- **Positioning:** [Investment / competitive / premium]
- **Value-Add Inclusions:** [Items to include at no extra charge]
- **Key Considerations:** [Risks, constraints, flexibility needed]

### Key Messages by Audience

| Audience | Primary Message | Supporting Evidence |
|---|---|---|
| Technical Evaluators | [Message] | [Evidence] |
| Management / Executives | [Message] | [Evidence] |
| Procurement / Contracts | [Message] | [Evidence] |

### Response Approach

- **Proposal Structure:** [Recommended outline aligned with evaluation criteria]
- **Tone:** [Consultative / authoritative / partnership-oriented]
- **Critical Success Factors:** [What must go right to win]
```

### 7. Save Output

Save the strategy brief to the working directory as `response_strategy.md` so the user can download it and it appears in the artifacts panel.

## Tools to Use

- **knowledge_base_retrieve**: Search for past proposals to similar clients, case studies, win/loss data, competitive intelligence, approved differentiators, and relationship history — search before developing win themes or competitive positioning
- **bash / str_replace_editor**: Read RFP evaluation criteria, scope, and background sections
- **grep**: Search for evaluation weighting, scoring methodology, incumbent references
- **glob**: Find all RFP-related documents including amendments and Q&A
