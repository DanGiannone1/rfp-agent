# Executive Summary Generation

## Purpose

Synthesize all RFP analysis, strategy, and drafted content into a compelling 1-2 page executive summary that captures evaluator attention and communicates Meridian & Associates LLP's value proposition clearly and persuasively.

## When to Use

- User asks for an "executive summary" or "exec summary"
- After other sections have been drafted (this section references and synthesizes them)
- As the final synthesis step before submission
- Can also be drafted early as a "strawman" to align the team, then refined later

## Step-by-Step Process

### 1. Gather Inputs

Before writing, review all available context:
- **Response strategy brief**: Win themes, competitive positioning, key messages
- **Requirements matrix**: Scope summary, compliance status, key requirements
- **Drafted sections**: Pull key points from technical approach, past performance, staffing, pricing
- **RFP evaluation criteria**: Ensure the summary addresses top-weighted factors
- **Customer pain points**: From the strategy analysis

Use `bash`, `glob`, and `str_replace_editor` to read these materials from the working directory.

### 2. Search KB for Supporting Evidence

Use `knowledge_base_retrieve` to find:
- Firm overview and branding language for Meridian & Associates LLP
- Headline metrics (years in business, number of professionals, client count, industry rankings)
- Most compelling case studies or client outcomes relevant to this opportunity
- Awards, recognitions, or differentiating certifications

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
- Reference specific past engagements with measurable outcomes
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

Save the completed executive summary to the working directory as `executive_summary.md` so the user can download it and it appears in the artifacts panel.

### 5. Refine for Impact

- **Length**: Keep to 1-2 pages (roughly 500-800 words unless RFP specifies otherwise)
- **Tone**: Confident but not arrogant; client-focused, not self-congratulatory
- **First sentence**: Must immediately engage — avoid generic openings
- **Every paragraph**: Should answer "why should the evaluator care?"
- **Metrics**: Include at least 2-3 quantified results or proof points
- **Consistency**: Win themes and key messages must match the rest of the proposal

## Output Format

```markdown
## Executive Summary

[Opening paragraph — demonstrate understanding of the client's situation, challenges, and objectives. Reference specific RFP language or client priorities.]

[Second paragraph — introduce Meridian's proposed approach and how it directly addresses the client's needs.]

### Our Approach

[High-level description of methodology, phasing, and key activities. Emphasize what makes the approach effective and tailored to this client.]

### Why Meridian & Associates LLP

[Win theme 1 with evidence. Win theme 2 with evidence. Demonstrate relevant experience, team quality, and commitment.]

[Reference specific past engagement: "In a similar engagement for [client type], Meridian [achieved specific outcome], resulting in [measurable benefit]."]

### Key Differentiators

| Differentiator | Client Benefit |
|---|---|
| [Differentiator 1] | [How this helps the client] |
| [Differentiator 2] | [How this helps the client] |
| [Differentiator 3] | [How this helps the client] |

### Our Commitment

[Closing paragraph — reaffirm commitment, express enthusiasm for the partnership, and invite further dialogue.]

---

*Note: This executive summary reflects the win themes and strategy outlined in the response strategy brief. Key metrics cited: [list sources for verification].*
```

## Tools to Use

- **bash / glob**: Read all previously drafted sections, strategy briefs, and RFP documents in the working directory
- **str_replace_editor**: Read and reference specific content from drafted sections
- **knowledge_base_retrieve**: Search for firm overview language, headline metrics, compelling case studies, branding guidelines, and approved boilerplate
- **grep**: Search for specific metrics, client names, or win themes across drafted content
