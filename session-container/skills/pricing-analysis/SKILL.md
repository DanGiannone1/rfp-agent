---
name: pricing-analysis
description: Build a pricing analysis and cost model with recommendations; use when asked for pricing or fee analysis.
---

# Pricing Analysis

## Purpose

Develop a structured pricing strategy and financial analysis for the proposed engagement. Includes cost modeling, sensitivity analysis, comparison to past engagements, and margin assessment. Produces a pricing summary that supports bid decisions and pricing negotiations.

## When to Use

- After response strategy is defined and before final proposal drafting, if that strategy artifact already exists
- User asks for "pricing analysis", "cost model", "ROI analysis", or "fee estimate"
- When evaluating whether an opportunity meets profitability thresholds
- When comparing pricing approaches for a competitive bid

## Step-by-Step Process

### 1. Gather Scope and Pricing Inputs

Read the RFP first to extract:
- Scope of services requested (service lines, deliverables, duration)
- Pricing format required (fixed fee, hourly, cost-plus, blended rates)
- Contract duration and renewal options
- Travel, technology, or other reimbursable requirements
- Any pricing constraints or ceilings mentioned
- Evaluation weight assigned to price vs. technical merit

Use existing strategy or requirements artifacts if they are already in the workspace, but do not require them before producing a pricing analysis.

### 2. Search Knowledge Base for Precedent

Use `knowledge_base_retrieve` to find:
- Rate cards and standard billing rates by grade/role
- Past proposals with similar scope and their pricing
- Historical actuals vs. estimates for comparable engagements
- Discount and margin guidance policies
- Cost model templates and fee estimation frameworks

Run multiple searches: "rate card", "pricing framework", "fee estimate [service area]", "cost model", "discount policy", "margin guidance".

### 3. Build the Cost Model

Construct a bottom-up cost estimate:

**Labor costs:**
- Identify required roles (partner, senior manager, manager, senior, staff)
- Estimate hours per role per phase
- Apply standard billing rates from KB
- Calculate blended rate

**Direct costs:**
- Travel and expenses (estimate based on engagement location, frequency)
- Technology/tools/licenses
- Subcontractor costs (if applicable)
- Report production and deliverable costs

**Indirect costs:**
- Overhead allocation
- Business development cost amortization
- Administrative support

### 4. Margin and Profitability Analysis

Calculate:
- **Gross margin**: (Revenue - Direct costs) / Revenue
- **Net margin**: (Revenue - All costs) / Revenue
- **Realization rate**: Effective rate vs. standard rate
- **Break-even point**: Minimum fee to cover costs
- Compare to firm targets (reference KB margin guidance)

### 5. Sensitivity Analysis

Model scenarios to understand risk:

| Scenario | Variable Changed | Impact on Margin |
|---|---|---|
| Base case | As estimated | [X]% margin |
| Scope creep (+20% hours) | Labor hours increase | [X]% margin |
| Rate pressure (-10% rates) | Billing rates reduced | [X]% margin |
| Timeline extension (+3 months) | Duration increases | [X]% margin |
| Staff mix shift (more senior) | Higher average rate | [X]% margin |

### 6. Competitive Price Positioning

Assess pricing relative to competition:
- **Price-to-win estimate**: What price point likely wins this work?
- **Value justification**: What premium can Meridian's quality/experience support?
- **Investment pricing**: Is a lower initial fee justified by follow-on potential?
- **Differentiating inclusions**: What value-adds offset a higher price?

### 7. Compare to Past Engagements

Use KB data to benchmark:
- Similar scope engagements and their final fees
- Actual hours vs. estimated hours on past projects
- Lessons learned on pricing accuracy
- Client price sensitivity history

## Output Format

```markdown
## Pricing & ROI Analysis

**RFP:** [Title / Number]
**Service Lines:** [Audit / Tax / Advisory]
**Contract Duration:** [Period]
**Pricing Format Required:** [Fixed fee / hourly / etc.]

### Cost Model Summary

| Category | Estimated Cost | % of Total |
|---|---:|---:|
| Partner | $[X] ([N] hrs @ $[rate]) | [X]% |
| Senior Manager | $[X] ([N] hrs @ $[rate]) | [X]% |
| Manager | $[X] ([N] hrs @ $[rate]) | [X]% |
| Senior Associate | $[X] ([N] hrs @ $[rate]) | [X]% |
| Staff | $[X] ([N] hrs @ $[rate]) | [X]% |
| **Total Labor** | **$[X]** | **[X]%** |
| Travel & Expenses | $[X] | [X]% |
| Technology/Tools | $[X] | [X]% |
| Subcontractors | $[X] | [X]% |
| **Total Direct Cost** | **$[X]** | **[X]%** |
| Overhead | $[X] | [X]% |
| **Total Cost** | **$[X]** | **100%** |

**Blended Rate:** $[X]/hr
**Total Hours:** [N]

### Profitability Assessment

| Metric | Value | Target | Status |
|---|---:|---:|:---:|
| Proposed Fee | $[X] | — | — |
| Gross Margin | [X]% | [X]% | PASS/WARN/FAIL |
| Net Margin | [X]% | [X]% | PASS/WARN/FAIL |
| Realization Rate | [X]% | [X]% | PASS/WARN/FAIL |
| ROI (fee / pursuit cost) | [X]:1 | [X]:1 | PASS/WARN/FAIL |

### Sensitivity Analysis

| Scenario | Fee Impact | Margin Impact | Risk Level |
|---|---:|---:|:---:|
| Base case | $[X] | [X]% | — |
| Scope creep (+20% hours) | $[X] | [X]% | Medium |
| Rate pressure (-10%) | $[X] | [X]% | High |
| Timeline extension | $[X] | [X]% | Medium |
| Staff mix shift | $[X] | [X]% | Low |

### Competitive Positioning

- **Recommended Price Point:** $[X]
- **Positioning:** [Investment / Competitive / Premium]
- **Price-to-Win Estimate:** $[X] range
- **Value Justification:** [Why our price is justified]

### Comparable Past Engagements

| Engagement | Scope | Proposed Fee | Actual Fee | Hours Variance |
|---|---|---:|---:|---:|
| [Past project 1] | [Similar scope] | $[X] | $[X] | [+/-X]% |
| [Past project 2] | [Similar scope] | $[X] | $[X] | [+/-X]% |

### Pricing Recommendation

[2-3 sentence summary: recommended fee, pricing model, key risks, and rationale]

### Action Items
1. [Items requiring human decision — e.g., partner approval on discounts, subcontractor quotes]
```

### 8. Save Output

Save the completed analysis to the working directory as `pricing_analysis.md` so the user can download it and it appears in the artifacts panel.

## Tools to Use

- **read_full_file**: Read RFP scope, pricing requirements, and evaluation criteria end-to-end
- **knowledge_base_retrieve**: Search rate cards, past engagement pricing, margin guidance, cost model templates, and discount policies
